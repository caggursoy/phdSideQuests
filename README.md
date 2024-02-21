# phdSideQuests
## A repository for side quests (i.e. projects) I've encountered (i.e. I plan to meddle with) during my PhD.

## Explanations for folders:

### labmeeting-protocol
An automated protocol poster for weekly KliPs department meetings.
Takes the info from a .docx file Ellen generates every week, posts its location for Linux/Windows paths and converts the .docx to a .png and posts to the dedicated channel for ease of access

### labmeeting-rocketchat
An automated reminder for weekly KliPs deparment meetings.
Can do the following:
- Reminds the persons who are scheduled to be the presenter/moderator in the next two meetings to present
- Posts next two labmeetings presenter/moderator tuple to a dedicated channel
- Every time there's an update in the KliPs labmeeting schedule repo, it reads the new labmeeting schedule and posts to the dedicated channel

### pug23Cal
Works only for PuG23 :)
Reads the PuG23 program from the PDF and pushes the events into a GCal where you can subsribe and follow from your apps!

### resmanToGCal
Just what we need!
We all know that Resman is awesome, but can only be accessed via ZI network.
This automaton filters your Resman entries and copies them to a dedicated GCal, so you can check your Resman appointments from your apps!

### rocket-greeter
ZI-ECRs RocketChat channel greeter!
This is the automaton that greets everyone who joins the ZI-ECRs main channel.