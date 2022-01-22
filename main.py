# from portfolio_page import github_api


def print_type(obj, key):
    type_name = type(obj[key]).__name__
    if obj[key] is None:
        type_name = "str"
    print(f"    {key}: {type_name}")


def generate_types_for_repository(repo):
    print("@dataclass")
    print("class User:")
    for key in repo['owner']:
        print_type(repo['owner'], key)

    print()
    print()
    print("@dataclass")
    print("class Repository:")
    for key in repo:
        print_type(repo, key)


def main():
    raw = True
    repos = github_api.get_repositories()

    if raw:
        # generate_types_for_repository(repos[0])
        for repo in repos:
            print(repo)
    else:
        for repo in repos:
            print(repo)


if __name__ == "__main__":
    main()
