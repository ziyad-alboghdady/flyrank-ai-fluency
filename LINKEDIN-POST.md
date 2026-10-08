# Build-in-public post

*One real decision, one real limitation. Paste-ready — swap the URL.*

---

I spent the last weeks building my portfolio, and the decision I keep getting asked about is the one where I **didn't** use my own stack.

I'm a backend engineer. ASP.NET Core is what I write. So the obvious move was to build the portfolio as a Razor Pages app on a free Azure tier — my stack, running live, proving itself.

I built it as static HTML instead.

The reasoning took me a while to accept. The site has nine pages. Its content changes when I finish a project — roughly four times a year. Its one dynamic need is a contact form. And it has to load, correctly, at 2am, when someone clicks the link on my CV. Which is the only moment it actually matters.

A running server buys flexibility I don't need and introduces downtime I can't afford. Static files on a CDN answer all three requirements and ask nothing of me between deploys.

The uncomfortable part: the more impressive-looking option was the wrong engineering call, and I wanted to make it anyway. Knowing when *not* to build a backend is part of being a backend engineer. So I put the reasoning on the site rather than hiding the decision.

And the limitation, because a post like this is worthless without one: the contact form depends on a third-party free tier. Fifty submissions a month, and their uptime isn't mine. I handled the failure path — if the request fails, the visitor sees my email address in plain text instead of a spinner — but I didn't eliminate the dependency, and I'm not going to pretend I did.

Site: [URL]

Built during the FlyRank AI Internship.

---

**Notes before posting**
- Keep it as one decision and one limitation. Resist adding a twelve-week summary — it dilutes both.
- If the stack decision feels stale by the time you post, swap in whichever decision is most honest on the day. The shape holds: *the obvious choice → why I rejected it → what it cost me → one thing still wrong.*
- Tag FlyRank. Don't tag more than that.
