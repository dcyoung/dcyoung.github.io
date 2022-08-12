---
title: "Generating Text & Poetry with AI"
date: 2018-01-01T00:00:00-00:00
last_modified_at: 2018-01-01T00:00:00-00:00
categories:
  - machine learning
  - ai
permalink: /post-generating-text-and-poetry/
classes: wide
excerpt: Generating text and poetry with language models.
header:
  og_image: https://assets.justinmind.com/wp-content/uploads/2018/11/Lorem-Ipsum-alternatives-768x492.png
  teaser: https://assets.justinmind.com/wp-content/uploads/2018/11/Lorem-Ipsum-alternatives-768x492.png
---

## Character Level RNN

For an over-the-top Valentine's day card, I trained a generative model to produce fake text messages. I trained the model on a brief history of shared text messages between me and my partner. The model was a character level sequential recurrent neural network, meaning it generated text by predicting the next most likely character (letter) following a sequence of characters. For example, if I wrote "happy birthda", you can guess the next character would like be "y". Obviously such a naive strategy of modeling language doesn't yield any long term coherence or structure, but I was hoping it might offer a few funny text messages.

Some unexpected challenges I encountered included

- scraping my own text messages from a cell phone (**WAY HARDER THAN IT SHOULD BE**)
- removing + replacing emojis and non-standard characters from the training data

Here are a few results:

![placeholder]()
​
...

And the source code: [https://github.com/dcyoung/numpy-char-rnn](https://github.com/dcyoung/numpy-char-rnn)

## Something far more powerful

My friend James is a writer. I love discussing generative AI, language modeling and linguistics with James. As a fun experiment, he offered some of his writings projects as training material, to see if we could create a text generation utility that could mimic his writing style.

For the task of modelling language, James' corpus of text was relatively tiny. I started by attempting to train the tiny model used in my Valentine's day bot, which learns to place characters one after another, without leveraging any grander model of language. This model had an effective working memory of ~50 characters, and would struggle to produce more than a coherent sentence.

To generate longer passages of coherent text, I turned to a ground breaking research project recently published by OpenAI. Read more: [GPT-2](https://openai.com/blog/better-language-models/). This model served as the baseline for modeling language. I then fine-tuned the model to learn the nuances of James' text. This process involved constraining the model by ONLY showing it samples from the tiny 3Mb of text data he provided.

Training took a few hours. In technical terms, I trained the model for 21500 `steps`.  During training (every 500 steps), I sampled random outputs from the model so I could see the output behavior as it learned. For each sample, a random prompt (literally random giberish) was provided as input, and the model produced 1023 character long passages as a continuation of this input. These are as close to "random unprompted thoughts" as I can get. While the quality definitely varies, I was blown away by the coherence of some passages. Here are a few snippets.

> And how our art replicates the patterns of the human heart more generally, treating everything with respect while at the same time offering an ultimatum toward life itself: be more attentive to this or else.

> "The wisest and clearest guidance I've ever received was from a man named Soren, who said, 'Close your eyes and imagine if you were to take one strand of your ancestry and cut it into thousands pieces; then when you were faced with your final piece, how would that feel?' He was being quite direct about this; I did as I was told and closed my eyes.

> We trace a painter out the back of a painting, all the while discovering that the work is in fact a series of staged performances, that this artist has put together to very swiftly show his audience what it's like to look at art. They've taken his canvas, wide eyed, and instead of painting people he's painted his own life as a montessori instructor.

> Yaardlsey was like the biggest punk band in the US, with Wyclef Jean on guitar and Arca on keys. He left Goth for Jameela, and they became the headliner of Burning Man . . . There was a point where he ended up burning the whole thing down to make it happen. There were reports of him raping Margarethe, so they put up a statue of her hanging from the rafters.
