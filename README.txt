The process is a bit of a mess right now. Will be more straightforward with a database.

When you want to update the reddit auto-posting events, follow this process:

1a. Copy over eventLibrary.js
1b. Change the export statement to "exports.eventLibrary = {..."
1c. Remove all require statements. The three file suffixes are .jpg, .jpeg, and .png
2. Copy over the eventPhotos folder
3. Run jsonConversion.js. This script takes in the eventLibrary and stringifies it, writing it to txtLibrary.txt
4. Run the apcRedditBot script (until you cron job it, anyway).

Thoughts for the future:

Give more descriptive titles (first sentence that does not begin with an asterisk?). 

If the event doesn't have a photo, do a self post?

Consider adding a tag comment on each event (could AutoMod it as well)