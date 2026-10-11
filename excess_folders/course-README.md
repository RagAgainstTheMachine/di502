## Welcome to DI 502: Data Informatics Course - Fall 2026

This repository holds the markdown templates for your project documentation as well as further instructions on setting up Confluence, Jira, and online resources to help build your project.

## Contents

- [How to start on Confluence](#how-to-start-on-confluence)
  - [Adding reviewer accounts](#adding-reviewer-accounts)
  - [Setting up Github actions workflow for Confluence integration](#setting-up-github-actions-workflow-for-confluence-integration)
- [Instructions on User Story Mapping and Sprint Planning](#instructions-on-user-story-mapping-and-sprint-planning)
- [How to start on Jira](#how-to-start-on-jira)
  - [Instructions on Jira Usage](#instructions-on-jira-usage)
- [Additional resources on Agile/Scrum](#additional-resources-on-agilescrum)

## How to start on Confluence

Below is an updated guide on how to set up your Confluence space and invite your team members and us onboard.

1. Ideally create a new Confluence instance using this [link](https://www.atlassian.com/try/cloud/signup?bundle=confluence&edition=free) if you have not created one.
2. Copy the link provided to invite your team members and us onto your Confluence space. (Link is valid for 30 days.) If you skip that step, you can manually invite members as such:
    1. Invite other collaborators from this link: **`[group_name].atlassian.net/admin/users`**
    2. To add them to your space, visit "space settings" for your project.
    3. Under space permissions click "users".
    4. Click "edit" and search for internal users. Add each collaborator.
    5. For each, click select all for permissions.

### Adding reviewer accounts

Each group must invite this email address to both their Confluence and Jira projects:

* [di.502.reviewer.1@proton.me](mailto:di.502.reviewer.1@proton.me)

And the reviewer account assigned to your specific team:

| Team        | Reviewer account                                                  |
|-------------|-------------------------------------------------------------------|
| Chunky      | [di.502.reviewer.2@proton.me](mailto:di.502.reviewer.2@proton.me) |
| Eliza | [di.502.reviewer.3@proton.me](mailto:di.502.reviewer.3@proton.me) |
| Promp Fiction   | [di.502.reviewer.4@proton.me](mailto:di.502.reviewer.4@proton.me) |
| Rag Against the Machine | [di.502.reviewer.5@proton.me](mailto:di.502.reviewer.5@proton.me) |

When adding reviewer accounts, consider giving them **read-only** access. (Managing permissions is only possible during the 30 day premium trial. After that you will be on the free plan.)

Whether you choose to send an invite link, or invite manually, please send a reminder to [volgas@metu.edu.tr](mailto:volgas@metu.edu.tr).

### Setting up Github actions workflow for Confluence integration

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens and choose Create API token (the classic kind, not "with scopes"). Copy it; Atlassian shows it only once.
2. In Github, go to Settings → Secrets and variables → Actions. On the Secrets tab, add: 
    * `CONFLUENCE_EMAIL`: Your user email
    * `CONFLUENCE_API_TOKEN`: The api token you created
3. On the Variables tab, add: 
    * `CONFLUENCE_BASE_URL`: `https://<site>.atlassian.net`
    * `CONFLUENCE_SPACE_KEY`: `KEY` in /wiki/spaces/<KEY>/… 
    * `DOCS_DIR`: `docs/Markdown Template` (Directory where the template lives in)

## Instructions on User Story Mapping and Sprint Planning

We recommend these resources if you haven't drafted a user story before:

* [User stories with examples and a template [Atlassian]](https://www.atlassian.com/agile/project-management/user-stories)
* [User stories [Ben Baumer, 5:31]](https://smith.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=2e293ab4-9faf-4550-8f94-acd8011132b1)

> [!TIP]
> We highly recommend using these collaborative tools:
> * [Miro](https://miro.com/) for user story mapping to identify which features are needed for your application,
> * [Scrum Powder - Sprint Planning](https://scrumpowder.com/planning) for story point estimation with poker planning and
> * [Scrum Powder - Retro](https://scrumpowder.com/retro) for having sprint retrospectives.

## How to start on Jira

1. Similarly, create a new Jira space with the default settings.
2. Click on the plus "+" icon in the header and add the "backlog" and "reports" pages.
3. Visit `Space settings -> Features` and enable Sprints as well as Estimation.
4. Set up your backlog to include four sprints that span the course.
5. Invite us and your team members to the Jira space in a similar manner.

### Instructions on Jira Usage

> [!TIP]
> We recommend taking at least one Jira course from those linked in Sprint 1 Fundementals of the [Online Course Register](online-course-register/README.md/#sprint-1-fundementals).

Once you create user stories and tasks associated with them, make sure to:

1. Assign specific people to the task, 
2. Define acceptance criteria in the description field, and 
3. Report the story point estimates in the "Story Point Estimate" field.

> [!WARNING]
> We don't recommend adding "subtasks" to divide big tasks as they cannot have story points and thus cannot be tracked. Make sure each task can be completed in one sprint (3 weeks) at most and by one member at least.

## Additional resources on Agile/Scrum
To be more familiar with Scrum framework, or Agile practices, be sure to check out the following websites and videos:

* https://www.atlassian.com/agile/scrum
* https://www.atlassian.com/agile/project-management/metrics
* https://www.youtube.com/watch?v=GR9-8lOUhwA (Introduction to Scrum) [scrum.org, 58:15]
* https://www.youtube.com/watch?v=wWSr3E2V6-Y (AI Is Making Teams Faster - And More Dangerous) [Mike Cohn, 9:01]
* https://www.youtube.com/watch?v=4wMRXmLpdA8 (AI in the SDLC: Rethinking AI Coding Tools & AI Agents) [IBM, 9:27]
