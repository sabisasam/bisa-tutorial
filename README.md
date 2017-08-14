# django-tutorial

## Tutorial part 4

The detail template got changed.
Previously it just listed the choices but now you can vote for a choice.
After a vote, another page with voting results is displayed.
To do this, the vote and results view got modified and a vote and results template got added.
Now the vote view adds 1 to the vote counter of the selected choice.
If the vote button got clicked and no choice was selected, the sentence "You didn't select a choice." appears above the choices.
The results view and its template show the question text, its choices with their number of votes and a link to the detail page of that question to vote again.
Finally the index, detail and results view were revised to use generic views.
