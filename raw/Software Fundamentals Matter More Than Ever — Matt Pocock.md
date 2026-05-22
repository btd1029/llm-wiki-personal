---
title: "\"Software Fundamentals Matter More Than Ever\" — Matt Pocock"
source: "https://www.youtube.com/watch?v=v4F1gFy-hqg"
author:
  - "[[AI Engineer]]"
published: 2026-04-24
created: 2026-05-17
description: "AI coding tools are overhyped and powerful at the same time. Used well, they're extraordinary. Used badly, they'll bury you in spaghetti code faster than any..."
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=v4F1gFy-hqg)

## Transcript

**0:07** · \[music\] Hello everyone. Having a good conference so far? Yeah. Are you having a good conference so far? Yeah. Good.

**0:20** · Wonderful.

**0:22** · I have a message for you that I hope will be um a comforting message for folks who believe that uh their skill set is no longer worth anything in this new age, which is I believe that software fundamentals matter now more than they actually ever have.

**0:39** · And I'm a teacher, and I've been recently teaching a course called Clojure Code for Real Engineers.

**0:47** · Nice and provocative. And in the process of kind of working on this course, I had to come up with a curriculum about AI coding, which is a bit of a nightmare because things are changing all the time, right? AI is a whole new paradigm.

**1:02** · We need to chuck out all of the old rules, surely, so that we can bring in the new stuff.

**1:08** · And there's a kind of movement that has come up around this, which is the specs-to-code movement. And the specs-to-code movement says that, "Okay, you can write a specification about how an application is supposed to work. Then you can use AI to turn it into code. If there's a problem with the application, you then go back to the spec. You don't really look at the code. You just change the spec, you run the compiler again, and you end up with more code." Raise your hand if you've heard of that.

**1:37** · Keep your hand raised if you've tried it.

**1:39** · Okay, I've tried it, too. You can put your hands down.

**1:42** · And what I noticed was I would run it, and I would try not to look at the code, but I would look at the code, and I realized I would get code out, first of all, and then I would run it, I would get worse code. And I did it again, I got even worse code. I got it again, I kept running the compiler, kept running the compiler, and I would just end up with garbage.

**2:03** · You know, raise your hand if that's happened to you.

**2:06** · Yes. I don't think this works. The idea that we can just ignore the code and just have the code let it manage itself is just sort of vibe coding by another name.

**2:16** · And I didn't believe that back then. I thought, "Okay, how do I fix the compiler? How do I make it so that it doesn't produce bad code each time, or worse code?"

**2:25** · And so I thought, "Okay, I need to explain to the LLM in English what a good code base looks like." Let me dig out one of my old favorite books, which is a Philosophy of Software Design by John Osterhout.

**2:37** · Go on Amazon, get it.

**2:39** · Um and he has a definition for what bad code looks like.

**2:45** · He calls it complex code. Complexity is anything related to the structure of a software system that makes it hard to understand and modify the system, right?

**2:53** · So a a bad code base is a code base that's hard to change. If you can't change a code base without causing bugs, then it's a bad code base. Good code bases are easy to change.

**3:04** · So I thought, "Ooh, that was good.

**3:05** · Let's try another book. Let's try The Pragmatic Programmer."

**3:08** · Go on Amazon, get it.

**3:10** · They have a whole chapter on something called software entropy. And this is exactly what I was seeing. Entropy is the idea that things tend towards um disaster and uh floating away from each other and collapse. And this is exactly how most software systems behave, too, is that every time you make a change to a code base, if you're only thinking about that change and not thinking about the design of the whole system, your code base is going to get worse and worse and worse. And that's what I was seeing.

**3:36** · Everything inside the specs-to-code idea that you just run the compiler again and again was making worse code.

**3:43** · Now, there's an idea that sort of drives the specs-to-code movement, which is that code is cheap. Raise your hand if you've heard that phrase before, that code is cheap. Yeah.

**3:55** · Well, I don't think this is right.

**3:57** · I think code is not cheap. In fact, bad code is the most expensive it's ever been.

**4:03** · Because if you have a code base that's hard to change, you're not able to take all of the bounty that AI can offer, cuz AI in a good code base actually does really, really well.

**4:15** · And this means good code bases matter more than ever, which means software fundamentals matter more than ever.

**4:20** · That's the thesis of this talk.

**4:22** · So let's actually get into practical stuff.

**4:25** · I'm going to talk about different failure modes that you may have experienced, or you may not have experienced yet with AI, and how you can avoid them by just going back to old books and looking at good software practices. Sound good?

**4:36** · So the first one is that the AI didn't do what I wanted.

**4:40** · You know, I I thought I had a good idea in my head, and the AI just did something totally different, or it did some uh like specs that I, you know, it just made something I didn't want. Raise your hand if you've hit this mode.

**4:51** · Cool. Okay.

**4:53** · Well, this is what they say in The Pragmatic Programmer, is that no one knows exactly what they want. It's that you and the AI, there is a communication barrier there, right?

**5:04** · And so when you're talking to the AI, that's kind of like the AI doing its requirements gathering. It's basically working out from you what it is that you need.

**5:12** · And I realized that there was another book, Frederick P. Brooks' The Design of Design, and it talks about this idea called the design concept.

**5:22** · It's that when you have more than one person designing something together, you have this idea sort of floating between you, this ephemeral idea of the thing that you're building. And that thing that you're building, or the idea of it, is called the design concept. It's not an asset, it's not something you can put in a markdown file, it is the invisible sort of theory of what you're building.

**5:44** · And so I thought, "Okay, that's what's going on. Me and the AI don't share a design concept." So I came up with a skill.

**5:51** · The skill is very, very simple. It's called Grill Me, and it looks like this.

**5:57** · "Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, which is another thing from Frederick P. Brooks, resolving dependencies between decisions one by one."

**6:10** · This skill is like uh the repo containing this skill has like 13,000 stars or something. Like, it just went nuts, went viral. People love this thing. It These couple of lines means the AI asks you like 40 questions, 60 questions. I've had it ask uh people 100 questions before it's satisfied they've reached a shared understanding. And it means it turns the AI into a kind of adversary, where it's just continually pinging you ideas and trying to reach a shared understanding.

**6:38** · And that means that the conversation that you then generate, you can take that and turn it into a product requirements document or something. Or if it's a small change, you can just uh do uh turn it directly into issues.

**6:52** · And then your AFK agent will then pick it up.

**6:54** · And don't at me on this, but I personally believe this is better than the default plan mode in uh the tool that I use, which is Clojure Code.

**7:04** · Plan mode is extremely eager to create an asset. It really wants to uh just create a plan and start working.

**7:12** · Whereas I think it's a lot nicer to reach a shared design concept first.

**7:18** · So that's tip number one.

**7:21** · Now, failure mode number two is that the AI is just way too verbose.

**7:25** · It's like you're almost talking at cross-purposes with the AI. Raise your hand if you uh feel this. If you've ever experienced that failure mode. Yeah.

**7:33** · It's kind of like the AI is like talking just using too many words to try to communicate what it's doing. It's not like you're talking uh using the same language.

**7:41** · And this to me felt very, very familiar, right? If you've ever been a developer for a long time, and you've worked with, let's say, domain experts, someone building an application, um let's say the domain expert wants you to build something on uh I don't know, microchips. You have no idea what microchips are.

**7:57** · You need to establish some kind of shared language, right? Cuz otherwise, they're going to be using terms you don't understand. You're going to be translating that into code that maybe you don't even understand, and certainly the domain expert won't.

**8:07** · And so there's this kind of language gap between you and the domain I went back to domain-driven design, DDD.

**8:17** · This is something I'm still kind of on the edge of exploring, but everything I'm reading about DDD is just music to my ears. I freaking love it.

**8:25** · And DDD has a concept of a ubiquitous language.

**8:30** · With a ubiquitous language, conversations among developers, and expressions of the code, and conversations with domain experts are all derived from the same domain model.

**8:39** · It's essentially a markdown file full of a list of terms that you and the AI have in common. And you really focus on those terms, and you really make sure that they're aligned with what it actually means, and you use them all the time in the code, when you're talking about the code, when you're talking to domain experts, or in our case, when you're talking with AI.

**8:57** · So I made a skill.

**8:59** · This skill is the ubiquitous language skill. Basically just scans your code base, looks for terminology, and then um creates a markdown file. Creates the ubiquitous language markdown file, a bunch of markdown tables with all of the terminology.

**9:14** · And this, then I pass it to the AI, and I'm able to read it, too. And I actually have it open all the time when I'm grilling with the AI and planning and that. What I noticed by reading the thinking traces of the AI, it not only improves the planning, but it allows the AI to think in a less verbose way, and actually means that the implementation is more aligned with what you actually planned. So this has absolutely been a powerhouse. It's been unbelievably good.

**9:41** · So that's tip number two. Create a shared language with the AI.

**9:45** · So okay, let's imagine that you've aligned with the AI. You know what it is you're supposed to be building. The AI has built the right thing, but it doesn't work.

**9:55** · Raise your hands if that's happened to you.

**9:57** · Yeah, just doesn't work.

**9:59** · Well, there's an obvious thing that we can do to make that better, which is we can use feedback loops. We can use um static types, you know, if you're not using TypeScript, uh that's crazy. Uh if you're not using uh if you're building a front-end app and you're not giving it the LLM access to the browser so it can look around, absolutely needs that.

**10:19** · And you obviously also need automated tests.

**10:23** · And one sort of thing I notice here is that even with these feedback loops, the LLM doesn't use them very well. It doesn't kind of like get the most out of its feedback loops in the way that a veteran developer would. And so it does what it tends to do is just does way too much at once. It will produce like a huge amounts of code and then think, "Oh, I should probably type check that actually." Or I should uh you know, maybe check a test on that or maybe do something like that.

**10:50** · And this in the Pragmatic Programmer they describe as outrunning your headlights. It's essentially driving too fast because the rate of feedback is your speed limit.

**11:02** · The rate of feedback is your speed limit, which means that you should be testing as you go, taking small deliberate steps. And the AI by default is really not very good at that.

**11:11** · So, skill number three is TDD.

**11:14** · You should be using test-driven development because TDD forces the LLM to really take small steps. You create a test first, you make that test pass, and then you refactor the code to make it nicer and consider the design.

**11:32** · The issue here is that testing is really hard.

**11:36** · Testing has always been hard.

**11:38** · And the reason for that is there are a ton of different decisions you need to make when you write a test.

**11:46** · You need to figure out how big a unit do you want to test?

**11:50** · You need to figure out what to mock. You need to figure out what behaviors do you even want to test in the first place?

**11:55** · And all of these decisions are dependent. So, if you are testing a really big unit like an entire uh massive application, then it might be quite flaky. You might not want to test that many behaviors. You know, if you only test this unit, you need to mock this unit, you know. It's all interlinked. And I've been thinking about this for years, for my entire development career.

**12:15** · And what we notice is that good codebases are easy codebases to test.

**12:20** · Right? So, here we're starting to get back to the idea of code being important. It's that the better your codebase is, the better your feedback loops are because you're able to um give better feedback to the LLM, it produces better code.

**12:35** · And so I thought, what does a good codebase, what does a testable codebase look like? Again, we go to John Ousterhout. \[clears throat\] He talks about having deep modules in your codebase. Not shallow modules, not lots of modules that expose type kind of um lots of functions.

**12:52** · They should be relatively few large deep modules with simple interfaces.

**12:57** · Let's compare them quickly.

**12:59** · Deep modules, lots of functionality hidden behind a simple interface. Hiding the complexity.

**13:05** · You can look inside the deep module if you want to, but you don't need to. You can just use the interface. Shallow modules, not much functionality, complex interface.

**13:13** · And I'll just wait for you to take the photos.

**13:18** · Shallow modules in a codebase kind of look like this, where you have a ton of different tiny little blobs that the AI has to walk through and navigate. And this is really hard for the AI to explore actually.

**13:30** · And so often what you'll see is if you have a codebase like this, which AI is really good at creating codebases like this, is that you'll have a situation where AI doesn't understand what your code is doing. It will attempt to explore the code, but because it's poorly laid out, filled with shallow modules, it doesn't maybe get to the right module in time or doesn't understand all the dependencies, all that stuff. It doesn't understand your code.

**13:53** · And so what does a codebase full of deep modules look like?

**13:57** · Well, it looks like this.

**14:00** · Where it's the same code, but it's just structured inside boundaries, where you have these interfaces on the top.

**14:08** · And these interfaces, you should probably have a lot of control over them and design them really well. Otherwise, you know, AI might mess up the design.

**14:17** · But the implementation, you can kind of leave that to the AI bit.

**14:20** · So, how do you turn a codebase that looks like this into a codebase that looks like that?

**14:29** · Well, I've got a skill for that. Improve codebase architecture. Turns out this is not It's it's quite complicated to do this, but it's a like a set of steps that you can reusably do again and again. You just sort of explore the codebase, look for opportunities where there's code that's kind of look um related, and wrap all of that in a deep module.

**14:50** · And this is a testable codebase because the boundaries around this code are so so simple. You test at the interface, you verify using that interface, and you're good to go. And so this is a codebase that rewards TDD.

**15:04** · But how about failure mode number six?

**15:06** · Which is your Okay, let's say your feedback loops are working. Let's say that things are kicking into gear.

**15:11** · You're able to ship more code than you ever have before, but your brain can't keep up.

**15:16** · Right? Uh raise your hand if you've felt more tired than you have ever before in your development career.

**15:22** · Yeah, me too. It's knackering.

**15:25** · And I think that this is a codebase that actually makes it harder for your brain because you, as well as the AI, need to keep all of that information in your head.

**15:34** · Whereas this, not only is it simpler for you to read and understand, it also means you can kind of treat these modules, or these deep modules, as gray boxes.

**15:47** · You can kind of say, "Okay, I'm going to just design the interface, but I'm not going to worry too much or not review the implementation too much."

**15:57** · You can do this obviously with uh things that are less critical in your application. Can't do this with uh you know, various things like finance or whatever, but in many many modules in your app, you don't need to think about the implementation too much as long as you have a testable boundary outside the module, and as long as you understand its purpose and can design it from the outside. I have found this has really saved my brain because I can just go, "Okay, the AI, I'll let you handle what's inside the big blob. I'm just going to test from the outside and verify it."

**16:26** · So, that's tip number five. Design the interface, delegate the implementation.

**16:32** · But this means that whenever we're touching the code, whenever we're planning stuff, we need to think about and be aware of the modules in our application. We need to know that map really well. It needs to be part of our ubiquitous language. We need to build it into our planning skills as well. So, my write a PRD, inside the PRD I'm specific about the module changes and the interfaces inside those modules, how they're being modified. I'm thinking about them all the time. And this comes from Kent Beck.

**16:58** · Invest in the design of the system every day.

**17:02** · And this is the core of it, right?

**17:03** · Because specs to code, we are not investing in the design of the system.

**17:08** · We are divesting from it. We're getting rid of that.

**17:12** · Whereas this, I think, is absolutely key.

**17:16** · And so code is not cheap. That's the message I want you to take away. Code is important.

**17:23** · And if we think about AI as a really great on-the-ground programmer, a kind of tactical programmer, a sergeant on the ground making the code changes, you need someone above that.

**17:35** · You need someone thinking on the strategic level. And that's you.

**17:39** · And that requires software fundamental skills that we've been using for 20 years, for longer.

**17:46** · Now, if you were interested in any of the skills I put up here, it's in the GitHub repo macpocockskills.

**17:52** · And if you're interested in the training that I do or any free stuff, I'm on YouTube, I'm on Twitter, but I'm also at aihero.dev, where I have a newsletter you can check out.

**18:01** · Thank you so much. I hope that this gives you confidence in this new AI age that you can actually make a good impact.

**18:07** · Thank you.

**18:09** · \[music\] \[applause\] \[music\] \[music\]