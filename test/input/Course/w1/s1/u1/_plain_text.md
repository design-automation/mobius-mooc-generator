# UNIT ==========
{:
  display_name="Unit 1 Just Text"
}

# COMPONENT ==========
{:
  type="html"
  display_name="Formatting Markdown"
}

# Markdown Cheatsheet

https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet

## Emphasis

Here are some tests for different formatting styles.

Emphasis, aka italics, with *asterisks* or _underscores_.

Strong emphasis, aka bold, with **asterisks** or __underscores__.

Combined emphasis with **asterisks and _underscores_**.

Strikethrough uses two tildes. ~~Scratch this.~~

## Links

[I'm an inline-style link](https://www.google.com)

[I'm an inline-style link with title](https://www.google.com "Google's Homepage")

[I'm a reference-style link][Arbitrary case-insensitive reference text]

[You can use numbers for reference-style link definitions][1]

Or leave it empty and use the [link text itself].

URLs and URLs in angle brackets will automatically get turned into links. 
http://www.example.com or <http://www.example.com> and sometimes 
example.com (but not on Github, for example).

Some text to show that the reference links can follow later.

[arbitrary case-insensitive reference text]: https://www.mozilla.org
[1]: http://slashdot.org
[link text itself]: http://www.reddit.com

## Images

Here's our logo (hover to see the title text):

Inline-style: 
![alt text](https://raw.githubusercontent.com/adam-p/markdown-here/master/src/common/images/icon1024.png "Logo Title Text 1")

Reference-style: 
![alt text][logo]

[logo]: https://raw.githubusercontent.com/adam-p/markdown-here/master/src/common/images/icon1024.png "Logo Title Text 2"

## Code

```javascript
var s = "JavaScript syntax highlighting";
alert(s);
```
 
```python
s = "Python syntax highlighting"
print s
```
 
```
No language indicated, so no syntax highlighting. 
But let's throw in a <b>tag</b>.
```

## Blockquotes

> Blockquotes are very handy in email to emulate reply text.
> This line is part of the same quote.

Quote break.

> This is a very long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote.

## Inline HTML

You can also use raw HTML in your Markdown, and it'll mostly work pretty well.

<dl>
  <dt>Definition list</dt>
  <dd>Is something people use sometimes.</dd>

  <dt>Markdown in HTML</dt>
  <dd>Does *not* work **very** well. Use HTML <em>tags</em>.</dd>
</dl>

## Horizontal Rule

Three or more...

---

Hyphens

***

Asterisks

___

Underscores

## Line Breaks

Here's a line for us to start with.

This line is separated from the one above by two newlines, so it will be a *separate paragraph*.

This line is also a separate paragraph, but...
This line is only separated by a single newline, so it's a separate line in the *same paragraph*.

# COMPONENT ==========
{:
  type="html"
  display_name="Plain Old Text and Some Code"
}

# Head 1

This is a test. Comp 2.

Here are some square brackets: [1,2,3]
Here are some arrow brackets: <4,5,6>
Did you know, 2 < 3 !

## Some Code 

Here is an example of some code.

~~~~~~~~~~~~~~~~~~~~~{.python hl_lines="3"}
# Here is how to draw a line
pos1 = make.Position([1,2,3])
pos2 = make.Position([1,2,3])
line = make.Polyline([pos1, pos2])
~~~~~~~~~~~~~~~~~~~~~


Youc an add extra attribute to your html like this. {: aaa=bbb }

# COMPONENT ==========
{:
    type="discussion"
    display_name="Discussion"
}
