# PLN Directory Portal API Documentation

**Base URL:** `{DIRECTORY_API_URL}/v1` (configured via environment variable)

**Authentication:** Most endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer {access_token}
```

---

## Table of Contents

1. [Authentication](#authentication)
2. [Members](#members)
3. [Teams](#teams)
4. [Projects](#projects)
5. [Asks](#asks)
6. [Office Hours / Member Interactions](#office-hours--member-interactions)
7. [Events (IRL/PL Events)](#events-irlpl-events)
8. [Events Submission](#events-submission)
9. [Search](#search)
10. [Home & Featured Content](#home--featured-content)
11. [Husky AI](#husky-ai)
12. [Profile](#profile)
13. [Forum](#forum)
14. [Locations](#locations)
15. [Skills & Focus Areas](#skills--focus-areas)
16. [Technologies](#technologies)
17. [Industry Tags](#industry-tags)
18. [Funding Stages](#funding-stages)
19. [Membership Sources](#membership-sources)
20. [Member Experiences](#member-experiences)
21. [Member Subscriptions](#member-subscriptions)
22. [Notification Settings](#notification-settings)
23. [LinkedIn Verification](#linkedin-verification)
24. [Join Requests](#join-requests)
25. [Participants Request](#participants-request)
26. [FAQ](#faq)
27. [OSO Metrics](#oso-metrics)
28. [Recommendations](#recommendations)
29. [Images](#images)
30. [Uploads](#uploads)
31. [Demo Days](#demo-days)
32. [Analytics](#analytics)
33. [Metrics](#metrics)
34. [Health](#health)
35. [Admin](#admin)
36. [Internals](#internals)

---

## Authentication

### Create Auth Request
**POST** `/v1/auth`

Creates an OAuth2 authentication request.

**Request Body:**
```json
{
  "state": "random_state_string"
}
```

**Response:**
```json
"uid_of_auth_request"
```

---

### Get Tokens
**POST** `/v1/auth/token`

Exchange authorization code or refresh token for access tokens.

**Request Body (Authorization Code):**
```json
{
  "grantType": "authorization_code",
  "code": "auth_code"
}
```

**Request Body (Refresh Token):**
```json
{
  "grantType": "refresh_token",
  "refreshToken": "your_refresh_token"
}
```

**Request Body (Token Exchange):**
```json
{
  "grantType": "token_exchange",
  "exchangeRequestToken": "token",
  "exchangeRequestId": "request_id"
}
```

**Response:**
```json
{
  "accessToken": "eyJhbGc...",
  "refreshToken": "eyJhbGc...",
  "idToken": "eyJhbGc...",
  "userInfo": {
    "uid": "member_uid",
    "email": "user@example.com",
    "name": "User Name",
    "profileImageUrl": "https://...",
    "roles": ["role1", "role2"],
    "leadingTeams": ["team_uid1"],
    "accessLevel": "L2",
    "isFirstTimeLogin": false
  },
  "isAccountLinking": false,
  "isEmailChanged": false,
  "isDeleteAccount": false
}
```

---

### Send OTP for Email Linking
**POST** `/v1/auth/otp`

**Auth Required:** Yes (UserAuthTokenValidation)

Sends OTP to email for account linking.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "otpToken": "otp_token_string"
}
```

---

### Resend OTP
**PUT** `/v1/auth/otp`

**Auth Required:** Yes (UserAuthTokenValidation)

**Request Body:**
```json
{
  "otpToken": "otp_token_from_previous_request"
}
```

**Response:**
```json
{
  "otpToken": "new_otp_token_string"
}
```

---

### Verify OTP and Link Account
**POST** `/v1/auth/otp/verify`

**Auth Required:** Yes (UserAuthTokenValidation)

**Request Body:**
```json
{
  "otp": "123456",
  "otpToken": "otp_token",
  "idToken": "id_token_from_auth"
}
```

**Response:**
```json
{
  "valid": true,
  "accessToken": "new_access_token",
  "refreshToken": "new_refresh_token",
  "idToken": "new_id_token",
  "userInfo": {
    "uid": "member_uid",
    "email": "user@example.com",
    "name": "User Name",
    ...
  }
}
```

---

### Delete External User Account
**POST** `/v1/auth/accounts/external/:id`

Deletes external user account.

**Request Body:**
```json
{
  "token": "external_auth_token"
}
```

**Response:**
```json
{
  "message": "Deleted successfully"
}
```

---

## Members

### Get Members (List)
**GET** `/v1/members`

Retrieves a list of members with filtering and pagination.

**Query Parameters:**
- Standard Prisma query builder params (filtering, sorting, pagination)
- `name__icontains` - Filter by name (case insensitive)
- `isHost` - Filter event hosts
- `isSpeaker` - Filter event speakers
- `isSponsor` - Filter event sponsors
- `officeHours__not=null` - Filter members with office hours
- `roles__in` - Filter by roles (comma-separated)
- `isRecent` - Filter recent members

**Response:** Array of member objects
```json
[
  {
    "uid": "member_uid",
    "name": "John Doe",
    "email": "john@example.com",
    "bio": "Software engineer...",
    "githubHandler": "johndoe",
    "discordHandler": "johndoe#1234",
    "twitterHandler": "johndoe",
    "telegramHandler": "johndoe",
    "linkedinHandler": "johndoe",
    "officeHours": "https://calendly.com/...",
    "ohStatus": "ACTIVE",
    "ohInterest": ["blockchain", "ai"],
    "ohHelpWith": ["development", "consulting"],
    "plnFriend": true,
    "isFeatured": false,
    "isVerified": true,
    "openToWork": true,
    "accessLevel": "L2",
    "createdAt": "2023-01-01T00:00:00Z",
    "updatedAt": "2023-06-01T00:00:00Z",
    "image": {
      "uid": "image_uid",
      "url": "https://...",
      ...
    },
    "location": {
      "uid": "location_uid",
      "city": "San Francisco",
      "country": "USA",
      ...
    },
    "skills": [{
      "uid": "skill_uid",
      "title": "JavaScript",
      ...
    }],
    "teamMemberRoles": [{
      "uid": "role_uid",
      "role": "Engineer",
      "team": {...},
      ...
    }],
    "projectContributions": [...],
    "experiences": [...]
  }
]
```

---

### Get Members by IDs
**POST** `/v1/members/by-ids`

Get multiple members by their UIDs.

**Request Body:**
```json
{
  "memberIds": ["uid1", "uid2", "uid3"]
}
```

**Response:** Array of simplified member objects
```json
[
  {
    "uid": "uid1",
    "name": "John Doe",
    "email": "john@example.com"
  }
]
```

---

### Get Members Bulk
**POST** `/v1/members/bulk`

Retrieve members by UIDs or external IDs (for NodeBB integration).

**Request Body:**
```json
{
  "memberIds": ["uid1", "uid2"],
  "externalIds": ["ext_id1", "ext_id2"]
}
```

**Response:** Array of member objects with complete details

---

### Get Member by UID
**GET** `/v1/members/:uid`

Get detailed information about a specific member.

**Query Parameters:**
- Standard Prisma query builder params for selecting relations

**Response:** Member object with all requested relations (same structure as list endpoint)

---

### Get Member by External ID
**GET** `/v1/members/external/:externalId`

Get member by their external authentication ID.

**Response:** Member object

---

### Get Member Roles with Counts
**GET** `/v1/members/roles`

Get list of roles with member counts for filtering.

**Query Parameters:** Same as Get Members

**Response:**
```json
[
  {
    "name": "Engineer",
    "count": 42
  },
  {
    "name": "Designer",
    "count": 15
  }
]
```

---

### Get Member Filters
**GET** `/v1/members/filters`

Get available filter options for members.

**Query Parameters:** Same as Get Members

**Response:**
```json
{
  "skills": [...],
  "locations": [...],
  "roles": [...],
  "teams": [...]
}
```

---

### Search Members (Advanced)
**GET** `/v1/members/search`

Advanced member search with office hours, topics, and role filtering.

**Query Parameters:**
- `q` - Search query
- `page` - Page number
- `limit` - Results per page
- `hasOfficeHours` - Boolean filter
- `topics` - Topics filter
- `roles` - Roles filter

**Response:**
```json
{
  "members": [...],
  "total": 100,
  "page": 1,
  "limit": 20
}
```

**Cache:** 5 minutes

---

### Autocomplete Topics
**GET** `/v1/members/autocomplete/topics`

Autocomplete topics from skills, experiences, office hours.

**Query Parameters:**
- `q` - Search query
- `page` - Page number (default: 1)
- `limit` - Results per page (default: 10)
- `hasOfficeHours` - Filter to members with office hours

**Response:**
```json
[
  "blockchain",
  "web3",
  "smart contracts"
]
```

**Cache:** 2 hours

---

### Autocomplete Roles
**GET** `/v1/members/autocomplete/roles`

Autocomplete roles from team member roles.

**Query Parameters:** Same as Autocomplete Topics

**Response:** Array of role strings

**Cache:** 2 hours

---

### Update Member
**PATCH** `/v1/members/:uid`

**Auth Required:** Yes (UserTokenValidation)

Update member information via participant request format.

**Authorization:**
- User can update their own profile
- Admin can update any profile
- Only admin can update `isVerified` field

**Request Body:**
```json
{
  "referenceUid": "member_uid",
  "newData": {
    "name": "New Name",
    "bio": "Updated bio",
    "githubHandler": "newhandle",
    "skills": ["skill_uid1", "skill_uid2"],
    "locationUid": "location_uid",
    ...
  }
}
```

**Response:** Updated member object

---

### Update Member (Direct)
**PUT** `/v1/members/:uid`

**Auth Required:** Yes (UserTokenValidation)

Direct update of member data.

**Authorization:** Same as PATCH endpoint

**Request Body:** Member update data

**Response:** Updated member object

---

### Get Member Preferences
**GET** `/v1/members/:uid/preferences`

**Auth Required:** Yes (AuthGuard - must be the member or admin)

Get member's preference settings.

**Response:**
```json
{
  "showEmail": true,
  "showGithubHandle": true,
  "showTelegram": false,
  "showLinkedin": true,
  "showDiscord": true,
  "showGithubProjects": true,
  "showTwitter": true,
  "showSubscription": false
}
```

---

### Update Member Preferences
**PATCH** `/v1/members/:uid/preferences`

**Auth Required:** Yes (AuthGuard - must be the member or admin)

Update member's preferences.

**Request Body:** Partial preferences object

**Response:** Updated preferences object

---

### Send OTP for Email Change
**POST** `/v1/members/email/otp`

**Auth Required:** Yes (UserAccessTokenValidateGuard)

Send OTP to new email for email change.

**Request Body:**
```json
{
  "newEmail": "newemail@example.com"
}
```

**Response:**
```json
{
  "otpToken": "otp_token_string"
}
```

---

### Update Member Email
**PUT** `/v1/members/email`

**Auth Required:** Yes (UserAccessTokenValidateGuard)

Update member's email after OTP verification.

**Request Body:**
```json
{
  "newEmail": "newemail@example.com",
  "otp": "123456",
  "otpToken": "otp_token"
}
```

**Response:** Updated member object

---

### Get Member GitHub Projects
**GET** `/v1/members/:uid/github/projects`

Get GitHub projects associated with a member.

**Response:**
```json
{
  "repositories": [
    {
      "name": "repo-name",
      "description": "Description",
      "url": "https://github.com/...",
      "createdAt": "2023-01-01T00:00:00Z",
      "updatedAt": "2023-06-01T00:00:00Z"
    }
  ]
}
```

---

## Teams

### Get Teams (List)
**GET** `/v1/teams`

Retrieves a list of teams with filtering.

**Query Parameters:**
- Standard Prisma query builder params
- `focusAreas` - Filter by focus areas
- `isHost` - Filter event hosting teams
- `isSponsor` - Filter event sponsor teams
- `officeHours__not=null` - Filter teams with office hours
- `isRecent` - Filter recent teams
- `askTags` - Filter by ask tags
- `orderBy=default` - Special ordering: teams with asks first

**Response:** Array of team objects
```json
[
  {
    "uid": "team_uid",
    "name": "Team Name",
    "logoUid": "image_uid",
    "blog": "https://blog.example.com",
    "website": "https://example.com",
    "contactMethod": "email@example.com",
    "twitterHandler": "teamhandle",
    "linkedinHandler": "teamhandle",
    "telegramHandler": "teamhandle",
    "shortDescription": "Brief description",
    "longDescription": "Detailed description",
    "plnFriend": true,
    "isFeatured": true,
    "officeHours": "https://calendly.com/...",
    "createdAt": "2023-01-01T00:00:00Z",
    "updatedAt": "2023-06-01T00:00:00Z",
    "logo": {...},
    "industryTags": [...],
    "fundingStage": {...},
    "technologies": [...],
    "teamMemberRoles": [...],
    "maintainingProjects": [...],
    "contributingProjects": [...],
    "teamFocusAreas": [...],
    "asks": [...]
  }
]
```

---

### Get Team by UID
**GET** `/v1/teams/:uid`

Get detailed information about a specific team.

**Query Parameters:**
- Standard Prisma query builder params for selecting relations

**Response:** Team object with requested relations

---

### Get Team Filters
**GET** `/v1/teams/filters`

Get available filter options for teams.

**Query Parameters:** Same as Get Teams

**Response:**
```json
{
  "industryTags": [...],
  "technologies": [...],
  "focusAreas": [...],
  "fundingStages": [...]
}
```

---

### Update Team
**PATCH** `/v1/teams/:uid`

**Auth Required:** Yes (UserTokenValidation + AccessLevelsGuard)
**Access Levels:** L2, L3, L4

Update team information.

**Authorization:**
- Must be team member or admin
- Uses participant request validation

**Request Body:**
```json
{
  "referenceUid": "team_uid",
  "newData": {
    "name": "Updated Team Name",
    "shortDescription": "New description",
    "industryTags": ["tag_uid1", "tag_uid2"],
    "technologies": ["tech_uid1"],
    ...
  }
}
```

**Response:** Updated team object

---

### Add/Edit Team Ask (Deprecated)
**PATCH** `/v1/teams/:uid/ask`

**Auth Required:** Yes (UserTokenValidation + AccessLevelsGuard)
**Access Levels:** L2, L3, L4

**Note:** Deprecated - use the `/v1/asks` endpoints instead

---

## Projects

### Get Projects (List)
**GET** `/v1/projects`

Retrieves a list of projects (excludes deleted projects).

**Query Parameters:**
- Standard Prisma query builder params
- `focusAreas` - Filter by focus areas
- `tags` - Filter by tags
- `isRecent` - Filter recent projects
- `askTags` - Filter by ask tags

**Response:** Array of project objects (excludes `isDeleted: true`)
```json
[
  {
    "uid": "project_uid",
    "name": "Project Name",
    "description": "Project description",
    "lookingForFunding": true,
    "logoUid": "image_uid",
    "logo": {...},
    "maintainingTeam": {...},
    "contributingTeams": [...],
    "projectFocusAreas": [...],
    "asks": [...],
    "createdAt": "2023-01-01T00:00:00Z",
    "updatedAt": "2023-06-01T00:00:00Z"
  }
]
```

---

### Get Project by UID
**GET** `/v1/projects/:uid`

Get detailed information about a specific project.

**Throws 404:** If project not found or is deleted

**Response:** Project object with full details

---

### Get Project Filters
**GET** `/v1/projects/filters`

Get available filter options for projects.

**Query Parameters:** Same as Get Projects

**Response:**
```json
{
  "focusAreas": [...],
  "tags": [...],
  "maintainingTeams": [...]
}
```

---

### Create Project
**POST** `/v1/projects`

**Auth Required:** Yes (UserTokenValidation + AccessLevelsGuard)
**Access Levels:** L2, L3, L4

Create a new project.

**Request Body:**
```json
{
  "name": "Project Name",
  "description": "Project description",
  "focusAreas": ["focus_area_uid"],
  "maintainingTeamUid": "team_uid",
  "contributingTeams": ["team_uid1", "team_uid2"],
  "lookingForFunding": false,
  ...
}
```

**Response:** Created project object

---

### Update Project
**PATCH** `/v1/projects/:uid`

**Auth Required:** Yes (UserTokenValidation + AccessLevelsGuard)
**Access Levels:** L2, L3, L4

Update an existing project.

**Request Body:** Partial project update data

**Response:** Updated project object

---

### Delete Project
**DELETE** `/v1/projects/:uid`

**Auth Required:** Yes (UserTokenValidation + AccessLevelsGuard)
**Access Levels:** L2, L3, L4

Soft deletes a project (sets `isDeleted: true`).

**Response:** HTTP 204 No Content

---

### Add/Edit Project Ask
**PATCH** `/v1/projects/:uid/ask`

**Auth Required:** Yes (UserTokenValidation + AccessLevelsGuard)
**Access Levels:** L2, L3, L4

Add or edit an ask for a project.

**Request Body:**
```json
{
  "title": "Ask title",
  "description": "Ask description",
  "tags": ["tag1", "tag2"]
}
```

**Response:** Updated project with ask

---

## Asks

### Get Ask by UID
**GET** `/v1/asks/:uid`

Get a specific ask with its relations (team, project, closedBy).

**Response:**
```json
{
  "uid": "ask_uid",
  "title": "Looking for developer",
  "description": "We need a full-stack developer...",
  "tags": ["engineering", "full-time"],
  "closedAt": null,
  "closedReason": null,
  "closedComment": null,
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-06-01T00:00:00Z",
  "team": {...},
  "project": {...},
  "closedBy": null
}
```

---

### Create Team Ask
**POST** `/v1/teams/:teamUid/asks`

**Auth Required:** Yes (UserTokenValidation)

Create a new ask for a team.

**Request Body:**
```json
{
  "title": "Ask title",
  "description": "Ask description",
  "tags": ["tag1", "tag2"]
}
```

**Response:** Created ask object

---

### Update Ask
**PATCH** `/v1/asks/:uid`

**Auth Required:** Yes (UserTokenValidation)

**Authorization:** Must be ask creator or team member/admin

Update an existing ask.

**Request Body:**
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "tags": ["newtag1"]
}
```

**Response:** Updated ask object

---

### Close Ask
**POST** `/v1/asks/:uid/close`

**Auth Required:** Yes (UserTokenValidation)

Close an ask with reason and comment.

**Request Body:**
```json
{
  "closedReason": "Resolved",
  "closedComment": "Issue was resolved",
  "closedByUid": "member_uid"
}
```

**Response:** Updated ask with closure info

---

### Delete Ask
**DELETE** `/v1/asks/:uid`

**Auth Required:** Yes (UserTokenValidation)

**Response:** HTTP 204 No Content

---

## Office Hours / Member Interactions

### Create Member Interaction
**POST** `/v1/office-hours/interactions`

**Auth Required:** Yes (UserTokenValidation)

Create a member-to-member interaction (e.g., booking office hours).

**Request Body:**
```json
{
  "targetMemberUid": "member_uid",
  "notes": "Would like to discuss blockchain development"
}
```

**Validation:**
- Cannot create interaction with yourself
- Rate limited (checks for recent interactions within configured interval)

**Response:**
```json
{
  "uid": "interaction_uid",
  "createdByUid": "creator_uid",
  "targetMemberUid": "target_uid",
  "notes": "...",
  "createdAt": "2023-01-01T00:00:00Z"
}
```

---

### Get Member Interaction Follow-ups
**GET** `/v1/office-hours/follow-ups`

**Auth Required:** Yes (UserTokenValidation)

Get follow-ups for interactions created by the logged-in user.

**Query Parameters:**
- `status` - Filter by status (comma-separated: PENDING, CLOSED)
- Standard Prisma query builder params

**Response:** Array of follow-up objects

---

### Create Member Interaction Feedback
**POST** `/v1/office-hours/interactions/:uid/feedback`

**Auth Required:** Yes (UserTokenValidation)

Provide feedback for an interaction follow-up.

**URL Parameters:**
- `:uid` - Follow-up UID

**Request Body:**
```json
{
  "rating": 5,
  "feedback": "Great session!",
  "happened": true
}
```

**Response:** Updated follow-up with feedback

---

### Close Member Interaction Follow-up
**POST** `/v1/office-hours/interactions/:interactionUid/follow-ups/:followUpUid/close`

**Auth Required:** Yes (UserTokenValidation)

Close a pending follow-up.

**Response:** Updated follow-up object

---

### Check All Office Hours Links (Batch)
**POST** `/v1/office-hours/check-all`

**Auth Required:** Yes (UserTokenValidation)

Batch check validity of all office hours links.

**Response:**
```json
{
  "checked": 150,
  "invalid": 5,
  "results": [...]
}
```

---

### Check Office Hours Link
**POST** `/v1/office-hours/check-link`

**Auth Required:** Yes (UserTokenValidation)

Check if a specific office hours link is valid.

**Request Body:**
```json
{
  "link": "https://calendly.com/..."
}
```

**Response:**
```json
{
  "valid": true,
  "status": "ACTIVE"
}
```

---

### Check Member Office Hours Link
**GET** `/v1/office-hours/members/:uid/check-link`

**Auth Required:** Yes (UserTokenValidation)

Check and update a specific member's office hours link.

**Response:**
```json
{
  "valid": true,
  "ohStatus": "ACTIVE"
}
```

---

### Report Broken Office Hours
**POST** `/v1/office-hours/members/:uid/report-broken`

**Auth Required:** Yes (UserTokenValidation)

Report that a member's office hours link is broken.

**Response:**
```json
{
  "reported": true,
  "message": "Report submitted successfully"
}
```

---

## Events (IRL/PL Events)

### Get PL Event Locations
**GET** `/v1/pl-events/locations`

Get all IRL event locations.

**Query Parameters:**
- Standard Prisma query builder params

**Response:** Array of event location objects

---

### Get PL Event by Slug
**GET** `/v1/pl-events/:slug`

**Auth Required:** Optional (UserAuthValidateGuard + AccessLevelsGuard)

Get event details by slug.

**Query Parameters:**
- `searchBy` - Search filter for guests
- Standard query params

**Response:** Event object with location, guests, and full details

---

### Get PL Event Guests by Location
**GET** `/v1/pl-events/locations/:uid/guests`

**Auth Required:** Optional (UserAuthValidateGuard + AccessLevelsGuard)

Get all guests for events at a specific location.

**Query Parameters:**
- `type` - Guest type filter (host, speaker, sponsor, attendee)

**Response:** Array of guest objects

---

### Get PL Event Topics by Location
**GET** `/v1/pl-events/locations/:uid/topics`

**Auth Required:** Optional (UserAuthValidateGuard)

Get all topics discussed at a location's events.

**Query Parameters:**
- `type` - Event type filter

**Response:** Array of topic strings

---

### Create PL Event Guest
**POST** `/v1/pl-events/locations/:uid/guests`

**Auth Required:** Yes (UserTokenValidation + AccessLevelsGuard)
**Access Levels:** L2, L3, L4

Add a guest to events at a location.

**Authorization:**
- Must be team member (if teamUid provided) or admin
- Admin can add to past events, others only to upcoming events

**Query Parameters:**
- `type` - Guest type (host, speaker, sponsor, attendee)

**Request Body:**
```json
{
  "memberUid": "member_uid",
  "teamUid": "team_uid",
  "events": ["event_uid1", "event_uid2"],
  "topics": ["topic1", "topic2"],
  ...
}
```

**Response:** Created guest object

---

### Update PL Event Guest
**PATCH** `/v1/pl-events/locations/:uid/guests/:guestUid`

**Auth Required:** Yes (UserTokenValidation + AccessLevelsGuard)
**Access Levels:** L2, L3, L4

Update a guest's information.

**Authorization:**
- Must be the guest themselves or admin

**Query Parameters:**
- `type` - Guest type

**Request Body:** Guest update data

**Response:** Updated guest object

---

### Delete PL Event Guests
**DELETE** `/v1/pl-events/locations/:uid/guests`

**Auth Required:** Yes (UserTokenValidation + AccessLevelsGuard)
**Access Levels:** L2, L3, L4

Delete multiple event guests.

**Authorization:**
- Admin only (unless deleting yourself)

**Request Body:**
```json
{
  "membersAndEvents": [
    {
      "memberUid": "member_uid",
      "eventUid": "event_uid"
    }
  ]
}
```

**Response:** Deletion confirmation

---

### Get PL Event Guest by UID and Location
**GET** `/v1/pl-events/locations/:uid/guests/:guestUid`

**Auth Required:** Yes (UserTokenValidation + AccessLevelsGuard)

Get specific guest details.

**Query Parameters:**
- `type` - Guest type

**Authorization:**
- Returns data for the guest if they are the logged-in user or if logged-in user is admin

**Response:** Guest object

---

### Get PL Event Guest Topics
**GET** `/v1/pl-events/locations/:uid/guests/:guestUid/topics`

**Auth Required:** Yes (UserTokenValidation + AccessLevelsGuard)

Get topics associated with a guest.

**Authorization:**
- Must be the guest or admin

**Response:** Array of topics

---

### Get PL Events by Logged-in Member
**GET** `/v1/pl-events/locations/:uid/member-events`

**Auth Required:** Yes (UserTokenValidation + AccessLevelsGuard)

Get all events the logged-in member is participating in at a location.

**Response:** Array of event objects

---

### Create PL Event by Location
**POST** `/v1/pl-events/locations/:uid/events`

**Auth Required:** Yes (AdminAuthGuard)

Create a new event at a location.

**Admin Only**

**Request Body:** Event creation data

**Response:** Created event object

---

### Delete Event
**DELETE** `/v1/pl-events/locations/:uid/events/:eventUid`

**Auth Required:** Yes (UserTokenValidation)

**Admin Only** - Delete an event.

**Response:** HTTP 204 No Content

---

### Sync PL Events by Location
**POST** `/v1/pl-events/sync`

**Auth Required:** Yes (InternalAuthGuard)

Sync events from external source (internal service only).

**Request Body:**
```json
{
  "selectedEventUids": ["event_uid1", "event_uid2"]
}
```

**Response:** Sync result summary

---

### Get All PL Event Guests
**GET** `/v1/pl-events/guests`

Get all event guests (no auth required).

**Response:** Array of all guest objects

---

### Get All Upcoming Events
**GET** `/v1/pl-events/upcoming`

Get all upcoming events across all locations.

**Response:** Array of upcoming event objects

---

### Get Event Contributors
**GET** `/v1/pl-events/contributors`

Get all teams/organizations that have contributed to events.

**Response:** Array of contributor team objects

---

### Get All Aggregated IRL Data
**GET** `/v1/pl-events/aggregated`

**Auth Required:** Optional (UserAuthValidateGuard + AccessLevelsGuard)

Get aggregated statistics for IRL events.

**Query Parameters:**
- Various filters for aggregation

**Response:**
```json
{
  "totalEvents": 50,
  "totalGuests": 500,
  "totalLocations": 10,
  "breakdowns": {...}
}
```

---

### Update IRL Aggregated Data Priority
**PATCH** `/v1/pl-events/aggregated/priority`

**Auth Required:** Yes (UserTokenValidation)

**Admin Only** - Update priority/ordering of aggregated data.

**Request Body:** Priority update data

**Response:** Updated aggregation

---

### Update PL Event Location
**PATCH** `/v1/pl-events/locations/:uid`

**Auth Required:** Yes (UserTokenValidation)

**Admin Only** - Update event location details.

**Request Body:** Location update data

**Response:** Updated location object

---

### Send Event Guest Presence Request
**POST** `/v1/pl-events/locations/:uid/presence-request`

**Auth Required:** Yes (UserTokenValidation + AccessLevelsGuard)
**Access Levels:** L2, L3, L4

Send presence confirmation request to event guests.

**Request Body:**
```json
{
  "eventUid": "event_uid",
  "guestUids": ["guest_uid1", "guest_uid2"]
}
```

**Response:** Email sending confirmation

---

## Events Submission

### Submit Event
**POST** `/v1/events`

**Auth Required:** Yes (UserTokenValidation)

Submit a new event for approval.

**Request Body:**
```json
{
  "name": "Event Name",
  "description": "Event description",
  "startDate": "2024-01-01T10:00:00Z",
  "endDate": "2024-01-01T18:00:00Z",
  "location": "San Francisco, CA",
  "url": "https://event.example.com"
}
```

**Response:** Created event submission object

---

## Search

### Full Text Search
**GET** `/v1/search`

Global search across all entities (members, teams, projects, etc).

**Query Parameters:**
- `q` - Search query (required)
- `strict` - Strict matching mode (boolean)

**Response:**
```json
{
  "members": [...],
  "teams": [...],
  "projects": [...],
  "focusAreas": [...],
  "total": 150
}
```

---

### Autocomplete Search
**GET** `/v1/search/autocomplete`

Autocomplete suggestions for global search.

**Query Parameters:**
- `q` - Search query (required)

**Response:**
```json
{
  "suggestions": [
    {
      "type": "member",
      "uid": "member_uid",
      "name": "John Doe"
    },
    {
      "type": "team",
      "uid": "team_uid",
      "name": "Team Name"
    }
  ]
}
```

---

## Home & Featured Content

### Get All Featured Data
**GET** `/v1/home/featured`

**Auth Required:** Optional (UserAuthValidateGuard)

Get featured content for homepage (teams, projects, members, events, locations).

**Response includes personalized data if user is logged in**

**Response:**
```json
{
  "teams": [...],
  "projects": [...],
  "members": [...],
  "events": [...],
  "locations": [...]
}
```

---

### Get Teams and Projects
**GET** `/v1/home/teams-and-projects`

Get teams and projects for homepage.

**Query Parameters:**
- Standard filtering params for teams and projects

**Response:**
```json
{
  "teams": [...],
  "projects": [...]
}
```

---

### Get All Discovery Questions
**GET** `/v1/home/discovery-questions`

Get discovery questions for Husky AI.

**Query Parameters:**
- Standard Prisma query builder params

**Response:** Array of discovery question objects

---

### Get Discovery Question by Slug
**GET** `/v1/home/discovery-questions/:slug`

Get a specific discovery question.

**Response:** Discovery question object

---

### Create Discovery Question
**POST** `/v1/home/discovery-questions`

**Auth Required:** Yes (UserTokenValidation)

**Admin Only** - Create a new discovery question.

**Request Body:**
```json
{
  "slug": "question-slug",
  "question": "Question text",
  "description": "Description"
}
```

**Response:** Created discovery question

---

### Update Discovery Question
**PATCH** `/v1/home/discovery-questions/:slug`

**Auth Required:** Yes (UserTokenValidation)

**Admin Only** - Update a discovery question.

**Request Body:** Discovery question update data

**Response:** Updated discovery question

---

### Update Discovery Question Counters
**PATCH** `/v1/home/discovery-questions/:slug/counters`

Increment share count or view count for a discovery question.

**Request Body:**
```json
{
  "attribute": "shareCount"
}
```

**Response:** Updated discovery question with new counter value

---

## Husky AI

### Husky Chat (Contextual)
**POST** `/v1/husky/chat/contextual`

Chat with Husky AI (streaming response).

**Request Body:**
```json
{
  "message": "Your question",
  "threadId": "thread_id"
}
```

**Response:** Server-sent events stream

---

### Husky Chat (Contextual with Tools)
**POST** `/v1/husky/chat/contextual-tools`

**Auth Required:** Optional (UserTokenCheckGuard)

Chat with Husky AI with tool calling capabilities (streaming JSON).

**Request Body:**
```json
{
  "message": "Your question",
  "threadId": "thread_id",
  "useTools": true
}
```

**Response:** Chunked JSON stream with tool invocations and AI responses

---

### Husky Chat Feedback
**POST** `/v1/husky/chat/feedback`

Submit feedback for a Husky AI response.

**Request Body:**
```json
{
  "threadId": "thread_id",
  "messageId": "message_id",
  "rating": 1,
  "feedback": "Optional feedback text"
}
```

**Response:**
```json
{
  "success": true
}
```

---

### Create Husky Thread
**POST** `/v1/husky/threads`

**Auth Required:** Yes (UserAccessTokenValidateGuard)

Create a new conversation thread.

**Request Body:**
```json
{
  "threadId": "client_generated_thread_id"
}
```

**Response:**
```json
{
  "threadId": "thread_id",
  "createdAt": "2023-01-01T00:00:00Z"
}
```

---

### Get Husky Threads
**GET** `/v1/husky/threads`

**Auth Required:** Yes (UserAccessTokenValidateGuard)

Get all threads for the logged-in user.

**Response:** Array of thread objects

---

### Get Husky Thread by ID
**GET** `/v1/husky/threads/:threadId`

**Auth Required:** Optional (UserTokenCheckGuard)

Get a specific thread with messages.

**Response:**
```json
{
  "threadId": "thread_id",
  "question": "Thread title",
  "messages": [
    {
      "role": "user",
      "content": "User message"
    },
    {
      "role": "assistant",
      "content": "AI response"
    }
  ],
  "createdAt": "2023-01-01T00:00:00Z"
}
```

---

### Duplicate Husky Thread
**POST** `/v1/husky/threads/:threadId`

**Auth Required:** Optional (UserTokenCheckGuard)

Duplicate an existing thread (for sharing).

**Request Body:**
```json
{
  "guestUserId": "optional_guest_user_id"
}
```

**Response:** New duplicated thread object

---

### Delete Husky Thread
**DELETE** `/v1/husky/threads/:threadId`

**Auth Required:** Yes (UserAccessTokenValidateGuard)

Delete a thread.

**Response:** HTTP 204 No Content

---

### Update Thread Basic Info
**POST** `/v1/husky/threads/:threadId/basic-info`

**Auth Required:** Yes (UserAccessTokenValidateGuard)

Update thread title/summary.

**Request Body:**
```json
{
  "question": "Thread title/question"
}
```

**Response:** Updated thread object

---

### Generate Member Bio
**GET** `/v1/husky/generation/bio`

**Auth Required:** Yes (UserAccessTokenValidateGuard)

Generate an AI-powered bio for the logged-in member based on their profile data.

**Response:**
```json
{
  "bio": "Generated bio text based on member's profile, skills, and experiences..."
}
```

---

### Generate Member Skills
**GET** `/v1/husky/generation/skills`

**Auth Required:** Yes (UserAccessTokenValidateGuard)

Generate suggested skills for the logged-in member based on their profile.

**Response:**
```json
{
  "skills": ["skill1", "skill2", "skill3"]
}
```

---

## Profile

### Get Profile Completeness Status
**GET** `/v1/profile/:memberUid/status`

**Auth Required:** Yes (UserTokenValidation)

Get profile completeness information for a member.

**Authorization:** Must be the member or admin

**Response:**
```json
{
  "completeness": 75,
  "missingFields": ["bio", "skills"],
  "suggestions": ["Add a bio", "Add your skills"]
}
```

---

## Forum

### Check Forum Group Access
**GET** `/v1/forum/check-group-access`

**Auth Required:** Optional (extracts token from request)

Check if user has access to forum groups (Protosphere integration).

**Response:**
```json
{
  "hasAccess": true
}
```

---

## Locations

### Get Locations
**GET** `/v1/locations`

Get all locations.

**Query Parameters:**
- Standard Prisma query builder params

**Response:** Array of location objects

---

### Validate Location
**POST** `/v1/locations/validate`

Validate and geocode a location using Google Places API.

**Request Body:**
```json
{
  "address": "123 Main St",
  "city": "San Francisco",
  "country": "USA"
}
```

**Response:**
```json
{
  "location": {
    "placeId": "ChIJ...",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "city": "San Francisco",
    "country": "United States",
    "continent": "North America"
  }
}
```

---

### Autocomplete Locations
**GET** `/v1/locations/autocomplete`

Autocomplete location suggestions.

**Query Parameters:**
- `q` - Search query
- Standard autocomplete params

**Response:** Array of location suggestion strings

---

### Get Location Details
**GET** `/v1/locations/:placeId`

Get detailed information about a location by Google Place ID.

**Response:** Location object with full details

---

## Skills & Focus Areas

### Get Skills
**GET** `/v1/skills`

Get all skills.

**Query Parameters:**
- Standard Prisma query builder params

**Response:** Array of skill objects

---

### Get Skill by UID
**GET** `/v1/skills/:uid`

Get a specific skill.

**Response:** Skill object

---

### Get Focus Areas
**GET** `/v1/focus-areas`

Get all focus areas.

**Query Parameters:**
- Custom query params for filtering

**Response:** Array of focus area objects

---

## Technologies

### Get Technologies
**GET** `/v1/technologies`

Get all technologies.

**Query Parameters:**
- Standard Prisma query builder params

**Response:** Array of technology objects

---

### Get Technology by UID
**GET** `/v1/technologies/:uid`

Get a specific technology.

**Response:** Technology object

---

## Industry Tags

### Get Industry Tags
**GET** `/v1/industry-tags`

Get all industry tags.

**Query Parameters:**
- Standard Prisma query builder params

**Response:** Array of industry tag objects

---

### Get Industry Tag by UID
**GET** `/v1/industry-tags/:uid`

Get a specific industry tag.

**Response:** Industry tag object

---

## Funding Stages

### Get Funding Stages
**GET** `/v1/funding-stages`

Get all funding stages.

**Query Parameters:**
- Standard Prisma query builder params

**Response:** Array of funding stage objects

---

### Get Funding Stage by UID
**GET** `/v1/funding-stages/:uid`

Get a specific funding stage.

**Response:** Funding stage object

---

## Membership Sources

### Get Membership Sources
**GET** `/v1/membership-sources`

Get all membership sources.

**Query Parameters:**
- Standard Prisma query builder params

**Response:** Array of membership source objects

---

### Get Membership Source by UID
**GET** `/v1/membership-sources/:uid`

Get a specific membership source.

**Response:** Membership source object

---

## Member Experiences

### Create Member Experience
**POST** `/v1/member-experiences`

**Auth Required:** Yes (UserTokenValidation)

Add a work experience to a member's profile.

**Request Body:**
```json
{
  "memberUid": "member_uid",
  "title": "Software Engineer",
  "company": "Company Name",
  "startDate": "2020-01-01",
  "endDate": "2022-12-31",
  "isCurrent": false,
  "description": "Job description"
}
```

**Validation:** `endDate` is required if `isCurrent` is false

**Response:** Created experience object

---

### Get Member Experience
**GET** `/v1/member-experiences/:uid`

Get a specific experience entry.

**Response:** Experience object

---

### Get Member Experiences by Member UID
**GET** `/v1/member-experiences/member/:memberUid`

Get all experiences for a member.

**Response:** Array of experience objects

---

### Update Member Experience
**PATCH** `/v1/member-experiences/:uid`

**Auth Required:** Yes (UserTokenValidation)

Update an experience entry.

**Request Body:** Experience update data

**Response:** Updated experience object

---

### Delete Member Experience
**DELETE** `/v1/member-experiences/:uid`

**Auth Required:** Yes (UserTokenValidation)

Delete an experience entry.

**Response:** HTTP 204 No Content

---

## Member Subscriptions

### Create Subscription
**POST** `/v1/member-subscriptions`

**Auth Required:** Yes (UserTokenValidation)

Create a new member subscription (following/notification preference).

**Request Body:**
```json
{
  "targetMemberUid": "member_uid",
  "subscriptionType": "FOLLOW"
}
```

**Response:** Created subscription object

---

### Modify Subscription
**PATCH** `/v1/member-subscriptions/:uid`

**Auth Required:** Yes (UserTokenValidation)

Update a subscription.

**Request Body:**
```json
{
  "subscriptionType": "MUTE"
}
```

**Response:** Updated subscription object

---

### Get Subscriptions
**GET** `/v1/member-subscriptions`

Get subscriptions based on query parameters.

**Query Parameters:**
- `memberUid` - Filter by subscriber
- `targetMemberUid` - Filter by target member
- Standard Prisma query builder params

**Response:** Array of subscription objects

---

## Notification Settings

### Get Notification Settings
**GET** `/v1/notification/settings/:memberUid`

**Auth Required:** Yes (UserTokenValidation)

Get notification preferences for a member.

**Authorization:** Must be the member

**Response:**
```json
{
  "emailNotifications": true,
  "weeklyDigest": true,
  "monthlyNewsletter": false,
  "recommendationsEnabled": true
}
```

---

### Update Notification Settings
**PATCH** `/v1/notification/settings/:memberUid`

**Auth Required:** Yes (UserTokenValidation)

Update notification preferences.

**Authorization:** Must be the member

**Request Body:** Partial notification settings object

**Response:** Updated settings object

---

### Update Recommendations Participation
**PUT** `/v1/notification/settings/:memberUid/participation`

**Auth Required:** Yes (UserTokenValidation)

**Admin Only** - Update member's participation in recommendations.

**Request Body:**
```json
{
  "recommendationsEnabled": true
}
```

**Response:** Updated settings

---

### Get Forum Notification Settings
**GET** `/v1/notification/settings/:memberUid/forum`

**Auth Required:** Yes (UserTokenValidation)

Get forum digest settings (from notification service).

**Authorization:** Must be the member

**Response:**
```json
{
  "forumDigestEnabled": true,
  "digestFrequency": "weekly"
}
```

---

### Update Forum Notification Settings
**PUT** `/v1/notification/settings/:memberUid/forum`

**Auth Required:** Yes (UserTokenValidation)

Update forum digest settings.

**Authorization:** Must be the member

**Request Body:** Forum notification settings

**Response:** Updated forum settings

---

### Get Notification Setting Item
**GET** `/v1/notification/settings/:memberUid/item/:type`

**Auth Required:** Yes (UserTokenValidation)

Get specific notification setting item.

**Query Parameters:**
- `contextId` - Context identifier

**Authorization:** Must be the member

**Response:** Notification setting item object

---

### Upsert Notification Setting Item
**PUT** `/v1/notification/settings/:memberUid/item/:type`

**Auth Required:** Yes (UserTokenValidation)

Create or update a notification setting item.

**Authorization:** Must be the member

**Request Body:** Notification item data

**Response:** Upserted notification item

---

## LinkedIn Verification

### Get LinkedIn Auth URL
**POST** `/v1/linkedin-verification/auth-url`

**Auth Required:** Yes (UserAccessTokenValidateGuard)

Get LinkedIn OAuth URL for verification.

**Authorization:** Must be the member

**Request Body:**
```json
{
  "memberUid": "member_uid",
  "redirectUrl": "https://app.example.com/callback"
}
```

**Response:**
```json
{
  "authUrl": "https://www.linkedin.com/oauth/v2/authorization?..."
}
```

---

### LinkedIn Callback
**GET** `/v1/linkedin-verification/callback`

Handle LinkedIn OAuth callback (redirects back to app).

**Query Parameters:**
- `code` - OAuth code
- `state` - State parameter

**Response:** Redirects to configured URL with verification status

---

### Get Verification Status
**GET** `/v1/linkedin-verification/status/:memberUid`

**Auth Required:** Yes (UserAccessTokenValidateGuard)

Get LinkedIn verification status for a member.

**Authorization:** Must be the member

**Response:**
```json
{
  "isVerified": true,
  "verifiedAt": "2023-01-01T00:00:00Z",
  "linkedinProfileUrl": "https://linkedin.com/in/..."
}
```

---

## Join Requests

### Submit Join Request
**POST** `/join-requests`

Submit a request to join the network (for new users).

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "reason": "I want to contribute to web3 projects",
  "referredBy": "Jane Doe"
}
```

**Response:**
```json
{
  "success": true
}
```

---

## Participants Request

### Add Participants Request
**POST** `/v1/participants-request`

**Auth Required:** Yes (UserAuthValidateGuard + AccessLevelsGuard)
**Access Levels:** L2, L3, L4

Add a new entry to the participants request table (for member/team updates).

**Request Body:**
```json
{
  "participantType": "MEMBER",
  "referenceUid": "member_uid",
  "newData": {...},
  "requesterEmailId": "requester@example.com"
}
```

**Response:** Created participants request object

---

### Add Member Request (Signup)
**POST** `/v1/participants-request/member`

Submit a new member signup request (creates member directly with L0 access).

**Request Body:**
```json
{
  "participantType": "MEMBER",
  "newData": {
    "name": "John Doe",
    "email": "john@example.com",
    ...
  }
}
```

**Response:**
```json
{
  "uid": "member_uid"
}
```

---

### Check Unique Identifier
**GET** `/v1/participants-request/unique-identifier`

Check if an identifier (email, team name) already exists.

**Query Parameters:**
- `type` - Identifier type (email, name, etc.)
- `identifier` - Value to check

**Response:**
```json
{
  "exists": true,
  "conflictType": "member"
}
```

---

## FAQ

### Submit Custom Question
**POST** `/faq`

Submit a custom FAQ question.

**Request Body:**
```json
{
  "question": "How do I join a team?",
  "email": "user@example.com",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "success": true
}
```

---

## OSO Metrics

### Get All OSO Metrics
**GET** `/v1/oso-metrics`

Get all OSO (Open Source Observer) metrics.

**Response:** Array of OSO metric objects

---

### Get OSO Metric by Project Name
**GET** `/v1/oso-metrics/:name`

Get OSO metrics for a specific project.

**Response:**
```json
{
  "projectName": "project-name",
  "activeDevs30Days": 15,
  "commits30Days": 120,
  "stars": 450,
  "forks": 75,
  ...
}
```

---

## Recommendations

### Get Unique Roles
**GET** `/v1/recommendations/settings/roles`

Get list of unique roles for recommendations settings.

**Response:**
```json
["Engineer", "Designer", "Product Manager", "Researcher"]
```

---

## Images

**Note:** This controller is marked as "for testing purposes only"

### Get All Images
**GET** `/v1/images`

Get all images.

**Response:** Array of image objects

---

### Get Image
**GET** `/v1/images/:uid`

Get a specific image.

**Response:** Image object

---

### Upload Image
**POST** `/v1/images/upload`

Upload an image file.

**Content-Type:** `multipart/form-data`

**Form Data:**
- `file` - Image file (JPEG, PNG, or WebP)

**Response:**
```json
{
  "uid": "image_uid",
  "url": "https://...",
  "cid": "ipfs_cid_or_s3_path",
  "filename": "hashed_filename.jpg",
  "createdAt": "2023-01-01T00:00:00Z"
}
```

**Storage:** IPFS or AWS S3 based on `FILE_STORAGE` env variable

---

## Uploads

### Upload File
**POST** `/v1/uploads`

**Auth Required:** Yes (UserTokenValidation)

Upload a file (image, video, slide, or other document).

**Query Parameters:**
- `kind` - Upload type: IMAGE, SLIDE, VIDEO, OTHER (default: OTHER)
- `scopeType` - Scope type: NONE, TEAM, MEMBER, PROJECT (default: NONE)
- `scopeUid` - UID of the scoped entity (required if scopeType is not NONE)

**Content-Type:** `multipart/form-data`

**Form Data:**
- `file` - File to upload

**Authorization:**
- For TEAM scope: Must be a member of the team
- For MEMBER/PROJECT scope: Must have appropriate permissions

**Response:**
```json
{
  "uid": "upload_uid",
  "storage": "S3",
  "kind": "IMAGE",
  "status": "READY",
  "scopeType": "TEAM",
  "scopeUid": "team_uid",
  "uploaderUid": "member_uid",
  "url": "https://...",
  "filename": "hashed_filename.jpg",
  "mimetype": "image/jpeg",
  "size": 102400,
  "checksum": "sha256_hash",
  "createdAt": "2023-01-01T00:00:00Z"
}
```

**Storage:** S3 or IPFS based on `FILE_STORAGE` env variable

---

### Get Upload
**GET** `/v1/uploads/:uid`

**Auth Required:** Yes (UserTokenValidation)

Get upload details by UID.

**Response:** Upload object with metadata

---

## Demo Days

### Get Current Demo Day
**GET** `/v1/demo-days/current`

**Auth Required:** Optional (UserTokenCheckGuard)

Get the current active or upcoming demo day with access information.

**Response:**
```json
{
  "uid": "demo_day_uid",
  "title": "Demo Day 2025 Q1",
  "description": "Quarterly demo day event",
  "startDate": "2025-03-15T10:00:00Z",
  "status": "ACTIVE",
  "userAccess": {
    "isParticipant": true,
    "participantType": "INVESTOR",
    "participantStatus": "ENABLED"
  }
}
```

---

### Get Current Demo Day Fundraising Profile
**GET** `/v1/demo-days/current/fundraising-profile`

**Auth Required:** Yes (UserTokenValidation)

Get the logged-in user's team fundraising profile for the current demo day.

**Response:**
```json
{
  "uid": "profile_uid",
  "teamUid": "team_uid",
  "demoDayUid": "demo_day_uid",
  "description": "Our team is building...",
  "onePagerUploadUid": "upload_uid",
  "videoUploadUid": "upload_uid",
  "onePagerUpload": {...},
  "videoUpload": {...},
  "team": {...},
  "createdAt": "2023-01-01T00:00:00Z"
}
```

---

### Get Current Demo Day Fundraising Profiles
**GET** `/v1/demo-days/current/fundraising-profiles`

**Auth Required:** Yes (UserTokenValidation)

Get all fundraising profiles for the current demo day (investor view).

**Query Parameters:**
- `stage` - Filter by funding stage (comma-separated)
- `industry` - Filter by industry tags (comma-separated)
- `search` - Search query

**Response:** Array of fundraising profile objects with team details

---

### Update Fundraising One-Pager
**PUT** `/v1/demo-days/current/fundraising-profile/one-pager`

**Auth Required:** Yes (UserTokenValidation)

Upload or update the team's one-pager for the current demo day.

**Content-Type:** `multipart/form-data`

**Form Data:**
- `onePagerFile` - PDF or slide file

**Response:** Updated fundraising profile

---

### Delete Fundraising One-Pager
**DELETE** `/v1/demo-days/current/fundraising-profile/one-pager`

**Auth Required:** Yes (UserTokenValidation)

Remove the team's one-pager.

**Response:** Updated fundraising profile

---

### Update Fundraising Video
**PUT** `/v1/demo-days/current/fundraising-profile/video`

**Auth Required:** Yes (UserTokenValidation)

Upload or update the team's pitch video for the current demo day.

**Content-Type:** `multipart/form-data`

**Form Data:**
- `videoFile` - Video file

**Response:** Updated fundraising profile

---

### Delete Fundraising Video
**DELETE** `/v1/demo-days/current/fundraising-profile/video`

**Auth Required:** Yes (UserTokenValidation)

Remove the team's pitch video.

**Response:** Updated fundraising profile

---

### Update Fundraising Description
**PUT** `/v1/demo-days/current/fundraising-profile/description`

**Auth Required:** Yes (UserTokenValidation)

Update the team's fundraising description.

**Request Body:**
```json
{
  "description": "Updated fundraising description"
}
```

**Response:** Updated fundraising profile

---

### Update Fundraising Team
**PATCH** `/v1/demo-days/current/fundraising-profile/team`

**Auth Required:** Yes (UserTokenValidation)

Update team selection for fundraising profile.

**Request Body:**
```json
{
  "teamUid": "team_uid"
}
```

**Response:** Updated fundraising profile

---

### Get Current Engagement
**GET** `/v1/demo-days/current/engagement`

**Auth Required:** Yes (UserTokenValidation)

Get user's engagement status with current demo day.

**Response:**
```json
{
  "uid": "engagement_uid",
  "demoDayUid": "demo_day_uid",
  "memberUid": "member_uid",
  "calendarAddedAt": "2023-01-01T10:00:00Z",
  "createdAt": "2023-01-01T00:00:00Z"
}
```

---

### Mark Calendar Added
**POST** `/v1/demo-days/current/engagement/calendar-added`

**Auth Required:** Yes (UserTokenValidation)

Track when user clicks "Add to Calendar" for demo day.

**Response:** Updated engagement object

---

## Analytics

Analytics events are tracked via the `Event` model for user behavior analysis. Events are typically tracked server-side via the AnalyticsService.

---

## Metrics

### Get Prometheus Metrics
**GET** `/metrics`

Get Prometheus metrics for monitoring.

**Response:** Prometheus-formatted metrics

---

## Health

### Health Check
**GET** `/health`

Get API health status.

**Response:**
```json
{
  "status": "ok",
  "info": {
    "prisma": {
      "status": "up"
    },
    "heroku": {
      "status": "up"
    }
  }
}
```

---

## Admin

### Admin Login
**POST** `/v1/admin/auth/login`

Login for back-office admin panel.

**Request Body:**
```json
{
  "username": "admin_username",
  "password": "admin_password"
}
```

**Response:**
```json
{
  "accessToken": "admin_jwt_token"
}
```

---

### Get Members (Admin)
**GET** `/v1/admin/members`

**Auth Required:** Yes (AdminAuthGuard)

Get members filtered by access levels (admin panel).

**Query Parameters:**
- `accessLevel` - Filter by access level
- `search` - Search query
- Standard pagination params

**Response:** Array of member objects with access level info

---

### Get Access Level Counts
**GET** `/v1/admin/members/access-level-counts`

**Auth Required:** Yes (AdminAuthGuard)

Get count of members by access level.

**Response:**
```json
{
  "L0": 50,
  "L1": 100,
  "L2": 75,
  "L3": 20,
  "L4": 5
}
```

---

### Update Access Level
**PUT** `/v1/admin/members/access-level`

**Auth Required:** Yes (AdminAuthGuard)

Update a member's access level.

**Request Body:**
```json
{
  "memberUid": "member_uid",
  "accessLevel": "L3"
}
```

**Response:** Updated member object

---

### Create Member (Admin)
**POST** `/v1/admin/members/create`

**Auth Required:** Yes (AdminAuthGuard)

Create a new member (admin only).

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "accessLevel": "L2",
  ...
}
```

**Response:** Created member object

---

### Edit Member (Admin)
**PATCH** `/v1/admin/members/edit/:uid`

**Auth Required:** Yes (AdminAuthGuard)

Edit member details (admin only).

**Request Body:** Member update data

**Response:** Member UID string

---

### Verify Members (Bulk)
**POST** `/v1/admin/members`

**Auth Required:** Yes (AdminAuthGuard)

Verify multiple members.

**Request Body:**
```json
{
  "memberIds": ["uid1", "uid2", "uid3"]
}
```

**Response:** Array of verification status objects

---

### Update Member and Verify
**PATCH** `/v1/admin/members/:uid`

**Auth Required:** Yes (AdminAuthGuard)

Update member from participants request and verify.

**Request Body:** Participants request data with updated member details

**Response:** Updated member object

---

### Get Participants Requests (Admin)
**GET** `/v1/admin/participants-request`

**Auth Required:** Yes (AdminAuthGuard)

Get all participants requests for admin review.

**Query Parameters:**
- `status` - Filter by status (PENDING, APPROVED, REJECTED)
- `participantType` - Filter by type (MEMBER, TEAM)
- Standard pagination

**Response:** Array of participants request objects

---

### Get Participants Request by UID (Admin)
**GET** `/v1/admin/participants-request/:uid`

**Auth Required:** Yes (AdminAuthGuard)

Get a specific participants request.

**Response:** Participants request object

---

### Update Participants Request (Admin)
**PUT** `/v1/admin/participants-request/:uid`

**Auth Required:** Yes (AdminAuthGuard)

Update a participants request.

**Request Body:** Updated request data

**Response:** Updated request object

---

### Process Participants Request
**PATCH** `/v1/admin/participants-request/:uid`

**Auth Required:** Yes (AdminAuthGuard)

Process (approve/reject) a participants request.

**Request Body:**
```json
{
  "status": "APPROVED",
  "isVerified": true
}
```

**Response:** Processing result

---

### Process Bulk Participants Requests
**POST** `/v1/admin/participants-request`

**Auth Required:** Yes (AdminAuthGuard)

Process multiple participants requests.

**Request Body:**
```json
[
  {
    "uid": "request_uid1",
    "status": "APPROVED"
  },
  {
    "uid": "request_uid2",
    "status": "REJECTED"
  }
]
```

**Response:** Bulk processing results

---

### Create Recommendation Run
**POST** `/v1/admin/recommendations/runs`

**Auth Required:** Yes (AdminAuthGuard)

Create a new recommendation run.

**Request Body:**
```json
{
  "targetMemberUid": "member_uid",
  "criteria": {...}
}
```

**Response:** Created recommendation run object

---

### Generate More Recommendations
**POST** `/v1/admin/recommendations/runs/:uid/generate-more`

**Auth Required:** Yes (AdminAuthGuard)

Generate additional recommendations for a run.

**Request Body:**
```json
{
  "count": 5
}
```

**Response:** Updated recommendation run

---

### Get Recommendation Runs
**GET** `/v1/admin/recommendations/runs`

**Auth Required:** Yes (AdminAuthGuard)

Get recommendation runs.

**Query Parameters:**
- `targetMemberUid` - Filter by target member
- `status` - Filter by status
- `unique` - Only unique runs

**Response:** Array of recommendation run objects

---

### Get Recommendation Run
**GET** `/v1/admin/recommendations/runs/:uid`

**Auth Required:** Yes (AdminAuthGuard)

Get a specific recommendation run.

**Response:** Recommendation run object with recommendations

---

### Update Recommendation Run Status
**PUT** `/v1/admin/recommendations/runs/:uid/status`

**Auth Required:** Yes (AdminAuthGuard)

Update recommendation run status.

**Request Body:**
```json
{
  "status": "SENT"
}
```

**Response:** Updated recommendation run

---

### Send Recommendations
**POST** `/v1/admin/recommendations/runs/:uid/send`

**Auth Required:** Yes (AdminAuthGuard)

Send recommendations to member via email.

**Request Body:**
```json
{
  "sendEmail": true
}
```

**Response:** Send confirmation

---

### Get Recommendation Notifications
**GET** `/v1/admin/recommendations/notifications`

**Auth Required:** Yes (AdminAuthGuard)

Get recommendation notification history.

**Query Parameters:**
- `targetMemberUid` - Filter by member

**Response:** Array of notification objects

---

### Get Members with Enabled Recommendations
**GET** `/v1/admin/recommendations/members-enabled`

**Auth Required:** Yes (AdminAuthGuard)

Get list of members who have recommendations enabled.

**Response:** Array of member objects

---

### Trigger Recommendations Job
**POST** `/v1/admin/recommendations/trigger-job`

**Auth Required:** Yes (AdminAuthGuard)

Manually trigger the recommendations cron job.

**Response:**
```json
{
  "message": "Recommendations job triggered successfully"
}
```

---

### Trigger Example Emails
**POST** `/v1/admin/recommendations/trigger-example-emails`

**Auth Required:** Yes (AdminAuthGuard)

Trigger example recommendation emails.

**Response:**
```json
{
  "message": "Example emails job triggered successfully"
}
```

---

### Create Demo Day
**POST** `/v1/admin/demo-days`

**Auth Required:** Yes (AdminAuthGuard)

Create a new demo day event.

**Request Body:**
```json
{
  "startDate": "2025-03-15T10:00:00Z",
  "title": "Demo Day 2025 Q1",
  "description": "Quarterly demo day event",
  "status": "upcoming"
}
```

**Response:** Created demo day object

---

### Get All Demo Days
**GET** `/v1/admin/demo-days`

**Auth Required:** Yes (AdminAuthGuard)

Get all demo days (including deleted).

**Response:** Array of demo day objects

---

### Get Demo Day Details
**GET** `/v1/admin/demo-days/:uid`

**Auth Required:** Yes (AdminAuthGuard)

Get detailed information about a specific demo day.

**Response:** Demo day object with participants

---

### Update Demo Day
**PATCH** `/v1/admin/demo-days/:uid`

**Auth Required:** Yes (AdminAuthGuard)

Update demo day information.

**Request Body:**
```json
{
  "startDate": "2025-03-20T10:00:00Z",
  "title": "Updated Title",
  "description": "Updated description",
  "status": "active"
}
```

**Response:** Updated demo day object

---

### Add Demo Day Participant
**POST** `/v1/admin/demo-days/:uid/participants`

**Auth Required:** Yes (AdminAuthGuard)

Add a single participant to a demo day.

**Request Body:**
```json
{
  "memberUid": "member_uid",
  "email": "investor@example.com",
  "name": "Investor Name",
  "type": "investor"
}
```

**Response:** Created participant object

---

### Add Demo Day Participants Bulk
**POST** `/v1/admin/demo-days/:uid/participants-bulk`

**Auth Required:** Yes (AdminAuthGuard)

Bulk import participants via CSV data.

**Request Body:**
```json
{
  "participants": [
    {
      "email": "investor1@example.com",
      "name": "Investor One",
      "investorProfile": {
        "type": "angel",
        "investmentFocus": ["web3", "ai"],
        "investInStartupStages": ["seed", "series-a"],
        "typicalCheckSize": 100000
      }
    }
  ]
}
```

**Response:**
```json
{
  "created": 10,
  "updated": 5,
  "errors": [],
  "participants": [...]
}
```

---

### Get Demo Day Participants
**GET** `/v1/admin/demo-days/:uid/participants`

**Auth Required:** Yes (AdminAuthGuard)

Get participants for a demo day with filtering and pagination.

**Query Parameters:**
- `page` - Page number
- `limit` - Results per page
- `status` - Filter by status (INVITED, ENABLED, DISABLED)
- `type` - Filter by type (INVESTOR, FOUNDER)
- `search` - Search query
- `sortBy` - Sort field
- `sortOrder` - Sort order (asc/desc)

**Response:**
```json
{
  "participants": [...],
  "total": 100,
  "page": 1,
  "limit": 20
}
```

---

### Update Demo Day Participant
**PATCH** `/v1/admin/demo-days/:demoDayUid/participants/:participantUid`

**Auth Required:** Yes (AdminAuthGuard)

Update participant status or team association.

**Request Body:**
```json
{
  "status": "enabled",
  "teamUid": "team_uid"
}
```

**Response:** Updated participant object

---

## Internals

**Note:** All internal endpoints require `INTERNAL_AUTH_TOKEN`

### Update Telegram UID
**PUT** `/v1/internals/members/telegram-uid`

**Auth Required:** Yes (InternalAuthGuard)

Update member's Telegram UID (internal service only).

**Request Body:**
```json
{
  "telegramHandler": "@username",
  "telegramUid": "123456789"
}
```

**Response:** Updated member object

---

## Common Response Codes

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `204 No Content` - Successful deletion
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid authentication token
- `403 Forbidden` - Authenticated but not authorized for this action
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Authentication Guards

The API uses several authentication guards:

1. **UserTokenValidation** - Validates user bearer token
2. **UserAuthValidateGuard** - Validates user auth (optional login supported)
3. **UserAccessTokenValidateGuard** - Validates access token with introspection
4. **AuthGuard** - Validates token and checks email matches resource owner
5. **AdminAuthGuard** - Requires admin privileges
6. **InternalAuthGuard** - Requires internal service token
7. **AccessLevelsGuard** - Checks user access level (L1-L4)
8. **UserTokenCheckGuard** - Checks for user token (guest access allowed)

---

## Access Levels

- **L0** - Newly signed up (pending approval)
- **L1** - Basic access (read-only)
- **L2** - Standard member access
- **L3** - Elevated member access
- **L4** - Team lead / high-level access
- **Admin** - Full administrative access

Most write operations require L2, L3, or L4 access levels.

---

## Rate Limiting & Caching

Some endpoints implement caching:
- Member search: 5 minutes
- Autocomplete endpoints: 2 hours
- Various read endpoints use query-based caching (default 24 hours)

Rate limiting is implemented for:
- Office hours interactions (configurable interval via `INTERACTION_INTERVAL_DELAY_IN_MILLISECONDS`)
- OTP requests
- Global rate limit: 10 requests per second per IP (configurable via ThrottlerModule)

---

## Environment Variables

Key environment variables used by the API:

- `DIRECTORY_API_URL` - Base URL for the directory API
- `AUTH_API_URL` - Auth service URL
- `AUTH_APP_CLIENT_ID` - OAuth client ID
- `AUTH_APP_CLIENT_SECRET` - OAuth client secret
- `WEB_UI_BASE_URL` - Frontend application URL
- `INTERNAL_AUTH_TOKEN` - Token for internal service calls
- `FILE_STORAGE` - Storage type (ipfs or aws)
- `INTERACTION_INTERVAL_DELAY_IN_MILLISECONDS` - Rate limit for interactions
- Many others (see .env.example file for complete list)

---

## Data Structures

### Common Schema Patterns

**Member Object:**
```json
{
  "uid": "string (cuid)",
  "name": "string",
  "email": "string",
  "externalId": "string | null",
  "imageUid": "string | null",
  "githubHandler": "string | null",
  "discordHandler": "string | null",
  "twitterHandler": "string | null",
  "telegramHandler": "string | null",
  "linkedinHandler": "string | null",
  "officeHours": "string | null",
  "ohStatus": "string | null",
  "ohInterest": "string[]",
  "ohHelpWith": "string[]",
  "bio": "string | null",
  "plnFriend": "boolean",
  "isFeatured": "boolean",
  "isVerified": "boolean",
  "openToWork": "boolean",
  "accessLevel": "string",
  "locationUid": "string | null",
  "createdAt": "string (ISO date)",
  "updatedAt": "string (ISO date)",
  "image": "Image | null",
  "location": "Location | null",
  "skills": "Skill[]",
  "teamMemberRoles": "TeamMemberRole[]",
  "projectContributions": "ProjectContribution[]",
  "experiences": "Experience[]"
}
```

**Team Object:**
```json
{
  "uid": "string (cuid)",
  "name": "string",
  "logoUid": "string | null",
  "blog": "string | null",
  "website": "string | null",
  "contactMethod": "string | null",
  "twitterHandler": "string | null",
  "linkedinHandler": "string | null",
  "telegramHandler": "string | null",
  "shortDescription": "string | null",
  "longDescription": "string | null",
  "plnFriend": "boolean",
  "isFeatured": "boolean",
  "officeHours": "string | null",
  "fundingStageUid": "string | null",
  "createdAt": "string (ISO date)",
  "updatedAt": "string (ISO date)",
  "logo": "Image | null",
  "industryTags": "IndustryTag[]",
  "membershipSources": "MembershipSource[]",
  "fundingStage": "FundingStage | null",
  "technologies": "Technology[]",
  "teamMemberRoles": "TeamMemberRole[]",
  "maintainingProjects": "Project[]",
  "contributingProjects": "Project[]",
  "teamFocusAreas": "TeamFocusArea[]",
  "asks": "Ask[]"
}
```

**Project Object:**
```json
{
  "uid": "string (cuid)",
  "name": "string",
  "description": "string | null",
  "lookingForFunding": "boolean",
  "logoUid": "string | null",
  "maintainingTeamUid": "string | null",
  "createdAt": "string (ISO date)",
  "updatedAt": "string (ISO date)",
  "logo": "Image | null",
  "maintainingTeam": "Team | null",
  "contributingTeams": "Team[]",
  "projectFocusAreas": "ProjectFocusArea[]",
  "asks": "Ask[]"
}
```

---

## Notes

1. **Prisma Query Builder**: Many list endpoints support advanced querying via a Prisma query builder that accepts filters, sorting, pagination, and relation selection through query parameters.

2. **Soft Deletes**: Projects use soft deletion (isDeleted flag) rather than hard deletion.

3. **Member Verification**: The `isVerified` field can only be modified by admins.

4. **Team Authorization**: Team-related write operations require being a team member or admin.

5. **IPFS/S3 Storage**: File uploads support both IPFS (decentralized) and AWS S3 storage based on `FILE_STORAGE` configuration.

6. **Streaming Responses**: Husky AI endpoints use streaming responses for real-time chat.

7. **External Services**: The API integrates with several external services:
   - Google Places API (locations)
   - GitHub API (member projects)
   - Protosphere/NodeBB (forum)
   - OpenAI (Husky AI)
   - Notification Service
   - Event Service
   - OSO (Open Source Observer)

8. **Response Entity IDs**: All responses use `uid` (CUID) for entity identification. Internal auto-increment `id` fields are hidden by the ConcealEntityIDInterceptor.

---

This documentation covers all major public API endpoints. For Swagger documentation, visit `/api/docs` when running the API locally.
