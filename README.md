# ops-github-toolbox
[Placeholder for Build Kite Badge](https://google.com.au)

## Usage:
- generate a personal token in your Github->settings->personal token _token_
- In your terminal, run `export GITHUB_TOKEN=<YOUR GITHUB TOKEN>`
- At same tab of the terminal, run `docker-compose run toolbox`
- Have a coffee or two, csv report will be generated.

## Problems trying to solve

### People Management

1 Rule enforcement

For security reasons, we need to enforce:
- 2FA, having email address on profile
- real name (FirstName LastName) on profile
- all machine users should be outside collaborators instead of members
- machine users should all be outside collaborators


2 Kick alumni out

It is hard for a large organisation's Github repository maintainers to know if an user in the Github organisation is no longer working for the org and should be removed.

3 New-Starter manual burden

New team members need to come to us repo maintainers to request write access. Ideally, new members should be given access automatically if their name could be found in Active Directory service. _And Dev Leads should be assigned as team admin who can self-manage_


### Team Management

- 1 tribe - 1 team

Github Teams are arbitrarily created, not ideally created by `1 tribe - 1 team ` policy.


### Repo Management

- Zombie Repos

It is time-consuming to tell which repositories have been collecting dust for years, and taking limited quota we have on Github. The quota costs, and zombie repos should be archieved.

- No repo backup procedure

We as an organisaion don't have automated process to backup/archieve Github repo to AWS-S3 buckets.
