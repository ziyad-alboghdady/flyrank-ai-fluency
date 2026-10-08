# Retrospective

*Written for the person I was in Week 1.*

You are about to write a proof statement, and you will write a paragraph. Then you will rewrite it as one sentence, and the one sentence will be better. That pattern repeats for twelve weeks: almost everything you produce is too long on the first pass, because you are trying to cover yourself rather than say the thing.

## What you set out to do

Build a portfolio that gets an engineering manager to invite you to a technical interview. That goal survived intact — which is unusual, and worth noticing. Most of what changed underneath it changed *because* the goal stayed fixed and kept rejecting things that did not serve it.

## What changed

**You assumed the portfolio would be an ASP.NET Core app, because that is what you build. It is static HTML.**

Working the stack decision properly — four constraints, three options, four pressure-test questions — produced an answer you did not want. Nine pages. Content that changes four times a year. One contact form. And an absolute requirement to be up at 2am, because that is when someone clicks the link on your CV. A running server buys flexibility you do not need and introduces downtime you cannot afford.

That was uncomfortable, and the discomfort is the lesson. The impressive-looking option was the wrong engineering call, and you wanted to make it anyway. Knowing when *not* to build a backend is part of being a backend engineer — and you would not have learned it by building the backend.

**You thought "AI fluency" meant better prompts. It is narrower than that: structure beats instruction.**

The prompt ladder made you better at asking. But the thing that actually changed how you work came out of the agent build. An agent told to "consider urgency" mentions urgency in passing and then does what it wanted. An agent that must produce a sentence naming *both* the score and the exam distance behaves correctly, every time. A shape someone has to fill is harder to skip than a factor they are supposed to weigh.

That is true of prompts, of API contracts, of DTOs, and of your own to-do list. It is the same instinct as validating at the DTO boundary instead of trusting the caller.

**You learned what you do not know by explaining things to people who know less than you.**

You used `preventDefault()` correctly for months without being able to say what it prevents. Nine lines of JavaScript on your own contact form exposed three gaps — one of which, `Accept` versus `Content-Type`, you had been getting away with because you had only ever seen content negotiation from the server side. You configure it in ASP.NET Core. You had never connected the two ends.

The explanation is the test. If you cannot teach it, you do not have it.

## What you would build next

Swap the Task Management API's persistence from `ConcurrentDictionary` to EF Core and PostgreSQL, and **count the files you have to change**.

The case study currently *claims* that decision is reversible — that it touches one class and one DI registration. Doing it turns the claim into evidence. And if it takes twelve files instead of three, that is the more interesting case study, and you should write that one instead.

## The three most transferable things

**1. Reversibility is worth more than correctness at the moment you decide.**
Persistence behind an interface. The site's URL behind a single `SITE` constant. The footer defined once, so the FlyRank badge lands on nine pages from one edit. None of those made the first version better. All of them made the second version cheap. Most of what looks like good architecture is just refusing to make decisions expensive to undo.

**2. Name the limitation before someone finds it.**
The contact form depends on a third-party free tier. The agent's grounding is only as good as what you remembered to upload. The site does not work opened straight from disk. Saying those out loud costs nothing and buys trust in everything else you claimed. The alternative is that a reviewer finds one themselves and starts quietly discounting the rest.

**3. A workflow you do not run is a diagram.**
You picked exam revision over a weekly industry brief for the automation assignment specifically because revision is non-negotiable and the brief was not. Same instinct applies to the portfolio: a recurring calendar event with a named action, not an intention to keep it updated.

## One thing you got wrong the whole way through

You consistently produced the polished version first and the honest version second. The rejection notes, the limitations sections, the fix logs — those turned out to be the parts reviewers found most convincing, and they were the parts you wrote last and nearly left out.

Next time, write those first.
