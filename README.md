levscrape
=========

Let's scrape the text witness statements of the Leveson Inquiry.

_This is a work in progress_

Done
----

* Parse a text transcript into a stream of _name_, _remark_, _time_.

Todo
----

* Screen scrape the [list of hearings](http://www.levesoninquiry.org.uk/hearings/)
* Run the parser on each hearing
* Convert output to an XML file using the [Akoma Ntoso specification](http://www.akomantoso.org/akoma-ntoso-in-detail/schema-1)
* Import into [MySociety](http://www.mysociety.org/)'s [SayIt](http://sayit.staging.mysociety.org/) ([code](https://github.com/mysociety/sayit))
