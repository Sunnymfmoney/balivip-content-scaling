# Automation troubleshooting

Work down the list. Do not skip to the bottom.

## The keyword does nothing

1. **Is the automation live?** Draft flows do not fire. Check the toggle.
2. **Is it scoped to the right post?** "Specific post" flows only fire on that post.
3. **Did you test from your own account?** ManyChat usually ignores the page owner.
   Test from an unrelated account.
4. **Did the comment actually contain the keyword?** Case usually does not matter,
   extra words usually do not, but emoji in the middle of a word will break it.
5. **Are permissions still granted?** Meta silently revokes on password change. Go to
   ManyChat settings and reconnect.
6. **Is the account a Business or Creator account?** Personal accounts cannot do this.

## The DM sends but nobody replies

Nobody is watching the inbox. That is a staffing problem, not a tooling problem. Name
one person.

## The link does not work

1. Open it on mobile data, not office wifi.
2. Check it is not a preview or staging URL.
3. Check the UTM parameters did not break the URL.
4. Check the page actually loads and the form actually submits. Submit a real test
   entry and confirm it arrives somewhere a human will see it.

## The copy and the destination do not match

This is the one that costs real money. Symptoms:

- The post says "comment VIP" and the automation listens for "BALI".
- The caption promises "no form" and the DM sends a form.
- The post says "link in bio" and the bio link is last month's.

**Fix:** open `automations/post-to-automation-map.md`, find the row, and make the post
match the row or the row match the post. Then re-test from a second account.

If a post is already live with a mismatch: edit the caption first, because that is
instant. Fixing the automation takes longer and the post keeps running meanwhile.

## Enquiries arrive but cannot be traced

No contact tag, or no UTM. Add both. Until they exist, "which post produced this
lead" is unanswerable and `analytics/` cannot do its job.

## Before you escalate

Have ready: the post link, the exact keyword, the automation name, a screenshot of
the flow, and the account you tested from. Without those the answer is always "test
it from a second account", which you could have done yourself.
