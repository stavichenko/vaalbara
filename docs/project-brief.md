# Project Brief — Vaalbara

## Concept

Vaalbara is a community platform that bridges the gap between spontaneous ideas and real-world events.
Users can propose ideas to gauge interest, collect votes,
and — when confidence is high enough — convert a validated idea into a location-bound event that others can join.

## Core Entities

### Idea
A lightweight proposal that a user puts forward to test its relevance with the community.

- Optionally tied to a location (global audience)
- Other users vote (like) to signal interest
- The author decides when enough votes justify moving forward
- Can be converted into an Event by the author

### Event (Initiative)
A concrete, location-bound happening that users can sign up to attend.

**Lifecycle stages:**
1. **Draft** — being prepared by the organizer
2. **Open** — accepting participants
3. **In Progress** — currently happening
4. **Completed** — finished
5. **Cancelled** — called off

Each event has an organizer (creator) and optionally a separate manager. Participants join with a specific role.

### Tags
Both Ideas and Events are tagged. Users subscribe to tags they care about and receive notifications when new Ideas or Events matching those tags are created or updated.

## Key Features

| Feature | Description |
|---|---|
| Idea validation | Post an idea, collect community votes, decide if it's worth running |
| Idea → Event conversion | One-click promotion of a validated idea into a full event |
| Location-aware events | Events are pinned to a geographic point; browse what's near you |
| Participant management | Users join events with defined roles |
| Tag subscriptions | Follow topics and get notified about matching ideas and events |
| Karma system | Users accumulate karma through contributions on the platform |
| Author as manager | Idea creator can choose to manage the resulting event themselves |

## Users

- **Regular user** — browses, votes on ideas, joins events
- **Organizer** — creates ideas and events, manages their own initiatives
- **Manager** — assigned to run an event on behalf of the organizer

## Tech Notes

- PostgreSQL with PostGIS for geographic queries
- UUIDs as primary keys throughout
- Phone and email verified separately; unique nicknames
