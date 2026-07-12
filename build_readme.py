"""Regenerate the recent-releases section of README.md."""
import json
import os
import pathlib
import re

from python_graphql_client import GraphqlClient

ROOT = pathlib.Path(__file__).parent.resolve()
CLIENT = GraphqlClient(endpoint="https://api.github.com/graphql")


TOKEN = os.environ.get("SOURCE_PUSH_TOKEN", "")


def replace_chunk(content, marker, chunk):
    """Replace the named marker block in content with the given chunk."""
    pattern = re.compile(
        rf"<!\-\- {marker} starts \-\->.*<!\-\- {marker} ends \-\->",
        re.DOTALL,
    )
    replacement = f"<!-- {marker} starts -->\n{chunk}\n<!-- {marker} ends -->"
    return pattern.sub(replacement, content)


def make_query(after_cursor=None):
    """Build the GraphQL query for the next page of repository releases."""
    after = f'"{after_cursor}"' if after_cursor else "null"
    return """
query {
  viewer {
    repositories(first: 100, privacy: PUBLIC, after:AFTER) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        name
        releases(last:1) {
          totalCount
          nodes {
            name
            publishedAt
            url
          }
        }
      }
    }
  }
}
""".replace("AFTER", after)


def fetch_releases(oauth_token):
    """Fetch the latest release for each public repo that has one."""
    repos = []
    collected_releases = []
    repo_names = set()
    has_next_page = True
    after_cursor = None

    while has_next_page:
        data = CLIENT.execute(
            query=make_query(after_cursor),
            headers={"Authorization": f"Bearer {oauth_token}"},
        )
        print()
        print(json.dumps(data, indent=4))
        print()
        for repo in data["data"]["viewer"]["repositories"]["nodes"]:
            already_seen = repo["name"] in repo_names
            if repo["releases"]["totalCount"] and not already_seen:
                repos.append(repo)
                repo_names.add(repo["name"])
                collected_releases.append(
                    {
                        "repo": repo["name"],
                        "release": repo["releases"]["nodes"][0]["name"]
                        .replace(repo["name"], "")
                        .strip(),
                        "published_at": repo["releases"]["nodes"][0][
                            "publishedAt"
                        ].split("T")[0],
                        "url": repo["releases"]["nodes"][0]["url"],
                    }
                )
        page_info = data["data"]["viewer"]["repositories"]["pageInfo"]
        has_next_page = page_info["hasNextPage"]
        after_cursor = page_info["endCursor"]
    return collected_releases


def main():
    """Fetch recent releases and rewrite them into README.md."""
    readme = ROOT / "README.md"
    releases = fetch_releases(TOKEN)
    releases.sort(key=lambda r: r["published_at"], reverse=True)
    markdown = "\n".join(
        f"* [{release['repo']} {release['release']}]"
        f"({release['url']}) - {release['published_at']}"
        for release in releases[:5]
    )
    readme_contents = readme.open().read()
    rewritten = replace_chunk(readme_contents, "recent_releases", markdown)

    readme.open("w").write(rewritten)


if __name__ == "__main__":
    main()
