import json
import os

from requests import request, Response

token = f"{os.getenv("GITHUB_API_TOKEN")}"

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-Github-Api-Version": "2026-03-10"
}

# response: Response = request(
#         method="GET",
#         url="https://api.github.com/repos/jellyfin/jellyfin/pulls?state=all&per_page=100&page=1",
#         headers=headers
#     )
#
# print(response.headers)

# pull_requests = []
# page = 1
#
issues_route = "https://api.github.com/repos/jellyfin/jellyfin/issues?state=all&per_page=100&page=1"
pulls_route = "https://api.github.com/repos/jellyfin/jellyfin/pulls?state=all&per_page=100&page=1"
commits_route = "https://api.github.com/repos/jellyfin/jellyfin/commits?per_page=100&page=1"

response: Response = request(
    method="GET",
    url=issues_route,
    headers=headers
)

parsed_data = json.loads(response.content)

with open("issues_data_sample.json", "w") as file:
    json.dump(parsed_data, file, indent=4)

response: Response = request(
    method="GET",
    url=pulls_route,
    headers=headers
)

parsed_data = json.loads(response.content)

with open("pulls_data_sample.json", "w") as file:
    json.dump(parsed_data, file, indent=4)

response: Response = request(
    method="GET",
    url=commits_route,
    headers=headers
)

parsed_data = json.loads(response.content)

with open("commits_data_sample.json", "w") as file:
    json.dump(parsed_data, file, indent=4)

# while True:
#     response: Response = request(
#         method="GET",
#         url=route,
#         headers=headers
#     )
#
#     parsed_data = json.loads(response.content)
#
#     pull_requests.extend(parsed_data)
#
#     next_link = response.links.get("next")
#     next_route = next_link.get("url") if next_link else None
#
#     if next_route:
#         route = next_route
#         if int(response.headers.get("X-RateLimit-Remaining", 0)) == 0:
#             reset_epoch = float(response.headers.get("X-RateLimit-Reset", 0))
#             if reset_epoch != 0.0:
#                 reset_time = datetime.datetime.fromtimestamp(reset_epoch, datetime.timezone.utc)
#                 current_time = datetime.datetime.now(datetime.timezone.utc)
#
#                 wait_time = (reset_time - current_time).total_seconds()
#
#                 time.sleep(wait_time)
#             else:
#                 raise Exception("Unable to parse headers for correct datetime")
#     else:
#         break
#
# print(len(pull_requests))
