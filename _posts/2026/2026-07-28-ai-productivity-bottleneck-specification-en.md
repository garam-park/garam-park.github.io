---
layout: post_with_ad
title: "The AI Productivity Bottleneck: I Started with the Specification, Not the Code"
date: 2026-07-28 19:12:08 +0900
last_modified_at: 2026-07-28 19:12:08 +0900
permalink: /en/20260728/ai-productivity-bottleneck-specification
categories: ai productivity collaboration
tags: [AI, productivity, requirements, specification, Notion, GitHub, collaboration]
lang: en
image: /images/2026/07/20260728-ai-requirements-specification-editorial.png
description: "A PoC showed that once AI accelerated implementation, interpreting requirements became the new bottleneck. This article explains how we used Notion and AI-assisted specification to reduce workflow risk concentrated in a single person."
excerpt: "The AI productivity bottleneck appeared before any code was written. This is what I learned from a PoC that used familiar Notion as a shared entry point and had AI turn ambiguous requests into questions and specifications."
---

[In the previous article](/en/20260719/ai-productivity-paradox), I explained how validation and decision-making can become new bottlenecks even when AI speeds up implementation. This time, I tried placing AI earlier in the process—at the stage where requirements are clarified—before any coding begins. The first thing we changed in the PoC was the process of turning requests from non-developers into specifications that developers could implement.

## I Thought Standardizing on GitHub Would Keep Things Simple

At first, I tried to standardize the process around GitHub, the tool AI handled best. Keeping everything—from requests and issues to pull requests and reviews—in one place seemed as though it would make context easier for AI to carry forward and simplify management. In hindsight, that choice optimized for the AI's convenience before considering how people actually worked.

But it was only simple from a developer's perspective.

For non-developers, GitHub was not a tool they needed in their day-to-day work. We were effectively asking people who already had plenty to do to learn a new tool and a new set of concepts just to submit a request. Their reluctance to learn GitHub may not have reflected a lack of cooperation; the benefit simply may not have justified the learning cost.

Yet the requests still had to go somewhere. In practice, a developer would listen, reinterpret the request, and transfer it to GitHub. This seemed faster in the short term. Over time, however, the context behind each request and the decisions made along the way began accumulating in one developer's experience and memory. Whenever that person was away or the work changed hands, their successor first had to reconstruct the context.

The person was not the problem. **The bottleneck was a structure in which work could move forward only after one particular person had interpreted and relayed it.**

## Instead of Standardizing the Tools, I Divided Their Roles

So instead of bringing every role into GitHub, I assigned each tool the job it handled best.

Notion, which the non-developers already used, became the entry point for requests and conversations. Using Notion did not make requirements clear by itself. It did, however, eliminate the need to learn another tool, while keeping requests and discussions together even when the person responsible changed.

We did not get rid of GitHub. Instead, we narrowed its use to the people responsible for implementation and review after a specification was finalized. GitHub remained the place where code changes were carried out and validated, rather than a shared space that everyone was expected to understand.

AI connected the two.

1. A non-developer submits a request in the Notion workspace they already know.
2. AI reads both the request and the existing code, then drafts a specification.
3. It asks about ambiguous points that could change the implementation outcome, one at a time.
4. A person reviews the options and makes the decision that best reflects the business intent.
5. Once the specification is finalized, implementation and review proceed in GitHub.

Rather than improvising this conversation each time, I made the process repeatable with two skills I created. The analysis skill examines a non-developer's request alongside the existing code and develops the requirements to an implementable level. The specification skill then confirms each expanded detail with a person to ensure it matches the business intent before finalizing the specification.

AI's role was not to copy sentences from Notion into a GitHub issue template. Its role was to turn the interpretation that once happened only in a particular developer's head into documented questions and specifications.

![Before-and-after diagram showing how a workflow that depended on one developer to interpret and relay requests was divided among Notion, AI analysis, human judgment, a finalized specification, and implementation and review in GitHub](/images/2026/07/ai-spec-workflow.svg){:style="width:100%"}

## One Short Phrase Changed the Implementation

We received a request to collect notifications from several sources on one screen. Stripped of any project-specific details, it looked something like this:

> Show multiple types of notifications in a list.<br>
> Show only today's notifications, with the newest first.

The general direction was understandable. But as soon as we tried to implement it, the word “today” proved ambiguous.

After examining the existing code and drafting a specification, the AI asked:

> Does “today” mean since midnight, or the past 24 hours from the current time?

With a calendar-day definition, the range of the list resets at midnight each day. With a rolling-time definition, the list retains all items from the preceding 24 hours. Either could be understood as “today,” but they produce different behavior.

![Diagram comparing a calendar-day interpretation of today, from midnight to the present, with a rolling-time interpretation covering the past 24 hours](/images/2026/07/ai-spec-today-vs-24hours.svg){:style="width:100%"}

Normally, a developer would likely have chosen whichever interpretation felt more familiar and implemented it. This time, AI made the distinction between the two options explicit, and a person selected the past 24 hours based on the business objective. AI did not make the correct decision for us; it brought the decision point forward, before implementation began.

That short exchange led us to clarify several conditions that were absent from the original request:

- Combine items from different sources into a single list.
- Display only items from the past 24 hours, ordered from newest to oldest.
- Define which timestamp represents the actual event time for each source.
- Decide how to handle items with missing or unparseable timestamps.
- Apply the same filter to both the on-screen list and the unread count.

A longer specification was not an achievement in itself. What mattered was finding the gaps a developer might otherwise have filled arbitrarily and turning them into choices a person could make before implementation.

## Earlier Decisions Reduced the Work That Followed

The first noticeable change was not faster implementation, but less work coming back. We needed fewer follow-up checks with the requester during implementation, and fewer tasks were sent back from QA because of conflicting interpretations.

The criteria for pull request reviews changed as well. When a specification is vague, reviewers tend to focus on whether the code is clean and whether there are any obvious errors. With clear completion criteria, a review agent can validate the implementation against the actual requirements.

- Are items from different sources included in the same list?
- Is the past-24-hours condition applied correctly?
- Are the list and the unread count based on the same data?
- Are invalid timestamps handled as agreed?

The specification was more than a document to show the requester. It became an implementation checklist, a basis for testing, and a contract defining what the review should verify.

AI did not create additional management overhead. It simply moved forward the decisions that would otherwise have been made late, during implementation or QA. There were slightly more questions, but less rework, and the criteria for implementation and review became clearer.

## Preserving Human Judgment While Reducing Dependence on Individuals

This process is not fully automated. AI reads the existing code and the request, then presents options, but a person decides which behavior matches the business intent. If the AI had quietly chosen “the past 24 hours,” that would not have been much different from a developer making an arbitrary interpretation.

What I wanted to reduce was not human judgment, but the risk of that judgment process existing only in one person's head.

Requests and conversations remain in Notion. AI turns ambiguous language into repeatable questions. People decide the direction of the work. The finalized specification is passed to those responsible for implementation and review in GitHub. Even when the people involved change, anyone can still look back and understand at least what was decided and why.

The conclusion of this article, therefore, is not that we “made AI handle development on its own.”

The goal was not to force everyone into a single tool. It was to let people submit requests and make decisions where they were already comfortable, have AI turn the ambiguity between those steps into a specification, and allow developers to focus on implementation and validation in GitHub.

> **The way to reduce the next bottleneck in AI productivity may not be to eliminate human judgment, but to surface it earlier and make it possible for someone else to carry it forward.**
