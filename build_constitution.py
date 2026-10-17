#!/usr/bin/env python3
"""Build the Asefa Family Gathering Constitution as a PDF (English + Amharic).

Run:  python3 build_constitution.py
Output: Asefa-Family-Gathering-Constitution.pdf in the same folder.

Edit the CONTENT_EN and CONTENT_AM lists below to change the text, then re-run.
Each item is one of:
  ("h1", text)              article heading
  ("p", text)               paragraph
  ("n", "1.", text)         numbered clause (hanging indent)
  ("b", text)               bullet under a clause
  ("t", rows, widths)       table; first row is the header; widths are in mm
  ("sig",)                  signature block
  ("pagebreak",)
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether,
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Asefa-Family-Gathering-Constitution.pdf")

# Kefa ships with macOS and covers Ethiopic script.
KEFA = "/System/Library/Fonts/Supplemental/KefaIII.ttf"
pdfmetrics.registerFont(TTFont("Kefa", KEFA))

DATE_EN = "17 October 2026"
DATE_AM = "ጥቅምት 7 ቀን 2019 ዓ.ም. (17 October 2026)"

# --------------------------------------------------------------------------
# ENGLISH CONTENT
# --------------------------------------------------------------------------
CONTENT_EN = [
    ("p", "This constitution governs the quarterly gathering of the grandchildren of Asefa. "
          "It is written so that every member knows what is expected, so that the gathering runs "
          "without waiting on anyone, and so that no member has cause to be angry at another. "
          "The English text is followed by an Amharic version. Where the two differ, the Gathering "
          "decides which text controls."),

    ("h1", "Article 1. Name and purpose"),
    ("n", "1.", "The association is called the Asefa Family Gathering (the \"Gathering\")."),
    ("n", "2.", "Its members are the grandchildren of Asefa, the children of his sons and daughters."),
    ("n", "3.", "The purpose of the Gathering is:"),
    ("b", "to keep the grandchildren of Asefa united as one family across generations;"),
    ("b", "to let the cousins and their children know one another and grow up together;"),
    ("b", "to support one another in times of joy and times of hardship;"),
    ("b", "to honour the memory and values of our grandfather Asefa and our parents."),
    ("n", "4.", "Every rule in this constitution serves the purpose above. When a rule is unclear, it is "
                "read in the way that best keeps the family in love and fairness."),

    ("h1", "Article 2. Membership"),
    ("n", "1.", "Every grandchild of Asefa who has reached the age of 18 is a member and is expected to join."),
    ("n", "2.", "A member's husband or wife is a family member of the Gathering. They are welcome at every "
                "program, may speak in discussions, and may host together with the member. They do not pay "
                "a separate contribution and do not vote, unless the Gathering decides otherwise by two-thirds."),
    ("n", "3.", "Children of members attend with their parents. When a child of a member reaches 18, they "
                "may join as a full member with the same rights and duties."),
    ("n", "4.", "A member living outside the city or abroad remains a member. Their attendance and "
                "contribution arrangement is set under Article 7."),
    ("n", "5.", "A member may leave by writing to the Secretary. A member who leaves receives no refund of "
                "past contributions, since the fund belongs to the Gathering as a whole."),
    ("n", "6.", "A member who has not paid contributions or fines for six months, after two written "
                "reminders, is suspended. A suspended member may return by paying what is owed."),
    ("n", "7.", "Every member has the same rights: to attend, to speak, to vote, to host, to stand for the "
                "committee, and to see the records."),

    ("h1", "Article 3. The gathering"),
    ("n", "1.", "The Gathering meets once every three months, on the first Saturday of that month."),
    ("n", "2.", "The program begins at 7:00 and ends at 11:00. The program starts at 7:00 whether or not "
                "every member has arrived. Nobody waits for anybody."),
    ("n", "3.", "The committee may move a date only for a death, a major holiday, or a national event, and "
                "must announce the new date at least two weeks ahead."),
    ("n", "4.", "Every program follows the same order so that it runs smoothly:"),
    ("t", [
        ["Time", "Item", "Led by"],
        ["7:00", "Opening and blessing", "Host"],
        ["7:10", "Welcome and roll call", "Secretary"],
        ["7:20", "Minutes of the last program and matters arising", "Secretary"],
        ["7:30", "Treasurer's report: contributions, fines, balance", "Treasurer"],
        ["7:45", "Family news: births, weddings, graduations, illness, needs", "Leader"],
        ["8:00", "Discussion items announced in advance", "Leader"],
        ["8:30", "Next host confirmed and date announced", "Leader"],
        ["8:40", "Meal, coffee and free time together", "Host"],
        ["10:45", "Closing words and thanks to the host", "Leader"],
        ["11:00", "Program ends", ""],
    ], [22, 108, 30]),
    ("n", "5.", "Any member who wants an item discussed sends it to the Secretary at least one week before "
                "the program. Items raised on the day are heard only if time allows."),
    ("n", "6.", "The formal part, from 7:00 to 8:40, is kept short and orderly so that the larger part of "
                "the day is for being together."),

    ("h1", "Article 4. Hosting"),
    ("n", "1.", "Each program is hosted by a married member in their own home, in the order fixed by lottery."),
    ("n", "2.", "The lottery is drawn once, in front of all members, and the Secretary records the full "
                "order. The order is not changed except as this article allows."),
    ("n", "3.", "Two hosts may swap turns by mutual agreement, with notice to the Secretary at least one "
                "month before the program."),
    ("n", "4.", "A host who cannot host on their turn for a serious reason tells the committee at least one "
                "month ahead. The next host in order steps forward, and the member who missed their turn "
                "hosts next."),
    ("n", "5.", "When every married member has hosted once, the cycle starts again in the same order. "
                "Members who married after the lottery are added at the end of the order."),
    ("n", "6.", "Unmarried members may volunteer to host or to co-host with a married member. A volunteer "
                "is added to the order at the next free turn."),
    ("n", "7.", "The host provides the place, the meal and the coffee ceremony, and keeps the program on "
                "time together with the Leader."),
    ("n", "8.", "Hosting is paid for by the host, as is our custom, but hosting is not a competition. The "
                "Gathering sets a reasonable spending guide so that no host feels pressured to outdo the "
                "last one. The Gathering may decide instead to pay a fixed hosting allowance from the fund."),
    ("n", "9.", "Every member thanks the host at the close of the program, and no member criticises the "
                "host's home or food."),

    ("h1", "Article 5. The committee"),
    ("n", "1.", "The Gathering is led by a committee of four: the Leader, the Deputy Leader, the Secretary "
                "and the Treasurer."),
    ("n", "2.", "Their duties are:"),
    ("b", "Leader: chairs the program, speaks for the Gathering, keeps order, and makes sure this "
          "constitution is followed."),
    ("b", "Deputy Leader: acts for the Leader when absent, and coordinates with the host before each program."),
    ("b", "Secretary: keeps the minutes, the attendance list, the hosting order and the fines register; "
          "sends notices and reminders."),
    ("b", "Treasurer: collects contributions and fines, keeps the ledger and the bank account, and reports "
          "at every program."),
    ("n", "3.", "The committee is elected by simple majority of members present at the first program of the "
                "year. Each serves a two-year term and may be re-elected once in a row. After that they rest "
                "for at least one term."),
    ("n", "4.", "Any member in good standing, with no unpaid dues, may stand for any post."),
    ("n", "5.", "The Gathering may remove a committee member by two-thirds vote for dishonesty, repeated "
                "absence, or neglect of duty, after hearing them."),
    ("n", "6.", "If a post falls vacant, the committee appoints a member to fill it until the next election."),
    ("n", "7.", "Committee members are not paid and are not exempt from contributions or fines."),

    ("h1", "Article 6. Finances"),
    ("n", "1.", "Every member contributes 700 birr each month. Payment is due by the 10th of the month, "
                "into the Gathering's bank account or to the Treasurer against a receipt."),
    ("n", "2.", "The Gathering keeps one bank account in its own name. Withdrawals need two signatures: "
                "the Treasurer and the Leader (or the Deputy Leader)."),
    ("n", "3.", "The fund is used only for:"),
    ("b", "support to a member at a wedding, a birth, a serious illness, or a death in their close family, "
          "in the amounts fixed in the support schedule;"),
    ("b", "an emergency loan to a member in hardship, approved by the Gathering and repaid on agreed terms;"),
    ("b", "joint family events and the running costs of the Gathering itself (stationery, receipts, bank charges);"),
    ("b", "any other purpose approved by two-thirds of members present."),
    ("n", "4.", "The support schedule is set by the Gathering and reviewed every year:"),
    ("t", [
        ["Event", "Support from the fund (birr)"],
        ["Wedding of a member", ""],
        ["Birth of a member's child", ""],
        ["Death of a member's parent, spouse or child", ""],
        ["Serious illness or hospital stay of a member", ""],
    ], [100, 60]),
    ("n", "5.", "No payment leaves the fund without a written request, the Treasurer's record and the "
                "Leader's approval. Payments above the schedule need a vote of the Gathering."),
    ("n", "6.", "The Treasurer reports at every program: contributions received, fines received, payments "
                "made, and the closing balance. The report is written and attached to the minutes."),
    ("n", "7.", "Two members who are not on the committee audit the ledger and the bank statements once a "
                "year and report to the Gathering."),
    ("n", "8.", "A contribution more than 30 days overdue carries a late fee of 100 birr per month."),
    ("n", "9.", "The Gathering may change the contribution amount by two-thirds vote. The change takes "
                "effect from the next quarter."),

    ("h1", "Article 7. Attendance and fines"),
    ("n", "1.", "Attendance at every program is a duty of membership."),
    ("n", "2.", "A member who cannot attend tells the Secretary at least three days before the program."),
    ("n", "3.", "Fines are as follows:"),
    ("t", [
        ["Situation", "Fine (birr)"],
        ["Absent without notice", "2,000"],
        ["Absent with notice given at least 3 days before", "1,000"],
        ["Absent for an excused reason (see clause 4)", "none"],
        ["Late by more than 30 minutes without notice", "200"],
        ["Disturbing the program after one warning from the Leader", "500"],
        ["Host cancelling their turn with less than one month's notice, without a serious reason", "1,000"],
    ], [130, 30]),
    ("n", "4.", "Excused reasons are: the member's own illness or the illness of their spouse or child; a "
                "death or funeral; a birth; work travel; an exam; and a national or religious duty. The "
                "Secretary records the reason. The committee may accept other serious reasons."),
    ("n", "5.", "Members living outside the city or abroad are excused from attendance and may join by "
                "video call. They continue to pay contributions unless the Gathering agrees a different amount."),
    ("n", "6.", "A fine is recorded by the Secretary on the day and announced at the next program. It is "
                "paid before or at the next program."),
    ("n", "7.", "A member who disputes a fine raises it with the committee within two weeks. The committee "
                "decides, and the member may appeal to the full Gathering under Article 10."),
    ("n", "8.", "A member with an unpaid fine does not vote until it is paid. Unpaid fines are treated like "
                "unpaid contributions under Article 2."),
    ("n", "9.", "Fines go into the fund and are reported together with the contributions."),

    ("h1", "Article 8. Code of conduct"),
    ("n", "1.", "We speak to one another with respect, as brothers and sisters. No insults, no shouting, no mocking."),
    ("n", "2.", "We respect the host's home as our own: we arrive on time, we help where asked, and we "
                "leave the place as we found it."),
    ("n", "3.", "Phones are on silent during the formal part of the program."),
    ("n", "4.", "Political and business arguments are not held during the program."),
    ("n", "5.", "Parents are responsible for their children's behaviour and safety."),
    ("n", "6.", "Alcohol, if served, is taken in moderation. A member who becomes disorderly is asked to "
                "leave and is fined under Article 7."),
    ("n", "7.", "What a member shares in confidence at the Gathering stays within the family."),
    ("n", "8.", "A member who has a complaint about another raises it under Article 10, not in front of "
                "the Gathering and not on social media."),
    ("n", "9.", "The Leader may give one warning for a breach. A second breach in the same program is "
                "fined. A pattern of breaches is brought to the Gathering, which may suspend the member "
                "for one program."),

    ("h1", "Article 9. Decisions and voting"),
    ("n", "1.", "The Gathering decides as a whole. The committee carries out decisions; it does not make "
                "them alone, except for day-to-day matters."),
    ("n", "2.", "Quorum: decisions are valid only when more than half of the members are present."),
    ("n", "3.", "Ordinary matters pass by simple majority of members present. A tie is decided by the Leader."),
    ("n", "4.", "These matters need two-thirds of members present: changing the contribution amount, "
                "changing a fine, spending above the support schedule, suspending or removing a member or "
                "a committee member, and amending this constitution."),
    ("n", "5.", "Voting is by show of hands. Any three members may ask for a secret ballot."),
    ("n", "6.", "Each member has one vote. There is no voting by proxy, except that a member abroad may "
                "vote in writing on a matter announced in advance."),
    ("n", "7.", "A matter once decided is not reopened for one year unless new facts arise."),

    ("h1", "Article 10. Settling disputes"),
    ("n", "1.", "Disagreements are expected in any family. What matters is how they are settled."),
    ("n", "2.", "The steps, in order:"),
    ("b", "Step 1. The two members talk privately and try to settle it themselves within two weeks."),
    ("b", "Step 2. If not settled, either member asks the committee in writing. The committee hears both "
          "within one month and proposes a settlement."),
    ("b", "Step 3. If either member rejects the committee's proposal, the matter goes to the full Gathering "
          "at the next program. The Gathering hears both and decides by simple majority. Both members "
          "leave the room during the vote."),
    ("b", "Step 4. If the dispute involves a committee member, or the Gathering's decision is not accepted, "
          "the matter goes to an elder of the parents' generation chosen by the Gathering. The elder's "
          "word is final."),
    ("n", "3.", "No dispute is discussed on social media or with people outside the family."),
    ("n", "4.", "A member who refuses to take part in these steps, or who takes a family dispute to "
                "outsiders, is fined 1,000 birr and may be suspended."),
    ("n", "5.", "When a dispute is settled, the two members shake hands before the Gathering, and the "
                "matter is closed and recorded."),

    ("h1", "Article 11. Records and transparency"),
    ("n", "1.", "The Secretary keeps the member register, the attendance list, the minutes of every "
                "program, the hosting order, and the fines register."),
    ("n", "2.", "The Treasurer keeps the contribution ledger, receipts, the bank statements, and the "
                "payments register."),
    ("n", "3.", "Minutes are read at the next program and approved by the members."),
    ("n", "4.", "Any member may ask to see any record at any time, and the committee shows it within one week."),
    ("n", "5.", "Records are kept in a shared folder, on paper and digitally, that passes to the next "
                "committee at every election."),
    ("n", "6.", "A copy of this constitution is given to every member, and to every new member on joining."),

    ("h1", "Article 12. Amendments and adoption"),
    ("n", "1.", "Any member may propose an amendment in writing to the Secretary. The proposal is "
                "announced at one program and voted on at the next, so that every member has three "
                "months to consider it."),
    ("n", "2.", "An amendment passes by two-thirds of members present and takes effect from the following program."),
    ("n", "3.", "This constitution is adopted when it is read in full at a program, approved by two-thirds "
                "of all members, and signed by the committee and the members present."),
    ("n", "4.", "Matters the Gathering must decide at adoption:"),
    ("b", "the hosting spending guide or hosting allowance (Article 4, clause 8);"),
    ("b", "the amounts in the support schedule (Article 6, clause 4);"),
    ("b", "whether spouses vote (Article 2, clause 2);"),
    ("b", "the contribution for members living abroad (Article 7, clause 5);"),
    ("b", "the elder for final appeal (Article 10)."),
    ("sig", {
        "title": "Adoption and signatures",
        "line": "Adopted on ____________________ at ____________________.",
        "cols": ["Post", "Name", "Signature"],
        "posts": ["Leader", "Deputy Leader", "Secretary", "Treasurer"],
        "members": "Members present",
        "mcols": ["No.", "Name", "Signature"],
    }),
]

# --------------------------------------------------------------------------
# AMHARIC CONTENT
# --------------------------------------------------------------------------
CONTENT_AM = [
    ("p", "ይህ መተዳደሪያ ደንብ የአሰፋ የልጅ ልጆች በየሦስት ወሩ የሚያደርጉትን የቤተሰብ ስብሰባ የሚመራ ነው። "
          "የተጻፈውም እያንዳንዱ አባል ከእሱ የሚጠበቀውን እንዲያውቅ፣ ስብሰባው ማንንም ሳይጠብቅ እንዲካሄድ፣ "
          "እንዲሁም አንዱ በሌላው ላይ የሚቆጣበት ምክንያት እንዳይኖር ነው። የእንግሊዝኛው ጽሑፍ የአማርኛ ቅጂ ይከተለዋል። "
          "ሁለቱ ሲለያዩ የትኛው እንደሚጸና ስብሰባው ይወስናል።"),

    ("h1", "አንቀጽ 1. ስም እና ዓላማ"),
    ("n", "1.", "ማኅበሩ \"የአሰፋ ቤተሰብ ስብሰባ\" (ከዚህ በኋላ \"ስብሰባው\") ተብሎ ይጠራል።"),
    ("n", "2.", "አባላቱ የአሰፋ የልጅ ልጆች፣ ማለትም የወንዶችና የሴቶች ልጆቹ ልጆች ናቸው።"),
    ("n", "3.", "የስብሰባው ዓላማ፦"),
    ("b", "የአሰፋን የልጅ ልጆች ከትውልድ ወደ ትውልድ እንደ አንድ ቤተሰብ አንድነታቸውን መጠበቅ፤"),
    ("b", "የአጎትና የአክስት ልጆች እና ልጆቻቸው እርስ በርስ እንዲተዋወቁና አብረው እንዲያድጉ ማድረግ፤"),
    ("b", "በደስታም በችግርም ጊዜ እርስ በርስ መደጋገፍ፤"),
    ("b", "የአያታችንን የአሰፋን እና የወላጆቻችንን መታሰቢያና እሴቶች ማክበር።"),
    ("n", "4.", "በዚህ ደንብ ውስጥ ያለ እያንዳንዱ ሕግ ከላይ ያለውን ዓላማ ያገለግላል። አንድ ሕግ ግልጽ ባልሆነ ጊዜ "
                "ቤተሰቡን በፍቅርና በፍትሕ በሚጠብቅ መንገድ ይተረጎማል።"),

    ("h1", "አንቀጽ 2. አባልነት"),
    ("n", "1.", "ዕድሜው 18 ዓመት የሞላው እያንዳንዱ የአሰፋ የልጅ ልጅ አባል ነው፤ እንዲቀላቀልም ይጠበቅበታል።"),
    ("n", "2.", "የአባል ባል ወይም ሚስት የስብሰባው የቤተሰብ አባል ነው። በእያንዳንዱ ፕሮግራም እንኳን ደህና መጡ ይባላሉ፣ "
                "በውይይት መናገር ይችላሉ፣ ከአባሉ ጋር አብረው ማስተናገድ ይችላሉ። የተለየ መዋጮ አይከፍሉም፤ ስብሰባው "
                "በሁለት ሦስተኛ ድምፅ ካልወሰነ በስተቀር ድምፅ አይሰጡም።"),
    ("n", "3.", "የአባላት ልጆች ከወላጆቻቸው ጋር ይገኛሉ። የአባል ልጅ 18 ዓመት ሲሞላው እኩል መብትና ግዴታ ያለው ሙሉ "
                "አባል ሆኖ መቀላቀል ይችላል።"),
    ("n", "4.", "ከከተማ ውጭ ወይም በውጭ አገር የሚኖር አባል አባልነቱ ይቀጥላል። የመገኘትና የመዋጮ ሁኔታው በአንቀጽ 7 "
                "መሠረት ይወሰናል።"),
    ("n", "5.", "አባል ለጸሐፊው በጽሑፍ በማሳወቅ መልቀቅ ይችላል። የለቀቀ አባል ያለፈ መዋጮው አይመለስለትም፤ ምክንያቱም "
                "ገንዘቡ የስብሰባው በሙሉ ንብረት ነው።"),
    ("n", "6.", "ለስድስት ወራት መዋጮ ወይም ቅጣት ያልከፈለ አባል፣ ሁለት የጽሑፍ ማስታወሻ ከተሰጠው በኋላ፣ ይታገዳል። "
                "የታገደ አባል ዕዳውን በመክፈል መመለስ ይችላል።"),
    ("n", "7.", "እያንዳንዱ አባል እኩል መብት አለው፦ የመገኘት፣ የመናገር፣ ድምፅ የመስጠት፣ የማስተናገድ፣ ለኮሚቴ "
                "የመወዳደር እና መዝገቦችን የማየት።"),

    ("h1", "አንቀጽ 3. ስብሰባው"),
    ("n", "1.", "ስብሰባው በየሦስት ወሩ አንድ ጊዜ፣ በዚያ ወር የመጀመሪያ ቅዳሜ ይካሄዳል።"),
    ("n", "2.", "ፕሮግራሙ በ7፡00 ይጀምራል፣ በ11፡00 ያበቃል። ሁሉም አባል ቢደርስም ባይደርስም ፕሮግራሙ በ7፡00 ይጀምራል። "
                "ማንም ማንንም አይጠብቅም።"),
    ("n", "3.", "ኮሚቴው ቀን የሚቀይረው ለሞት፣ ለትልቅ በዓል ወይም ለአገራዊ ጉዳይ ብቻ ሲሆን፣ አዲሱን ቀን ቢያንስ ከሁለት "
                "ሳምንት በፊት ማሳወቅ አለበት።"),
    ("n", "4.", "እያንዳንዱ ፕሮግራም በተመሳሳይ ቅደም ተከተል ይካሄዳል፦"),
    ("t", [
        ["ሰዓት", "ጉዳይ", "የሚመራው"],
        ["7፡00", "መክፈቻ እና ምርቃት", "አስተናጋጅ"],
        ["7፡10", "እንኳን ደህና መጣችሁ እና የተገኙ አባላት ጥሪ", "ጸሐፊ"],
        ["7፡20", "የባለፈው ስብሰባ ቃለ ጉባኤ እና ከዚያ የሚነሱ ጉዳዮች", "ጸሐፊ"],
        ["7፡30", "የገንዘብ ያዥ ሪፖርት፦ መዋጮ፣ ቅጣት፣ ቀሪ ሂሳብ", "ገንዘብ ያዥ"],
        ["7፡45", "የቤተሰብ ዜና፦ ልደት፣ ሠርግ፣ ምረቃ፣ ሕመም፣ ፍላጎቶች", "መሪ"],
        ["8፡00", "አስቀድመው የታወቁ የውይይት ጉዳዮች", "መሪ"],
        ["8፡30", "ቀጣዩ አስተናጋጅና ቀን ይገለጻል", "መሪ"],
        ["8፡40", "ምግብ፣ ቡና እና አብሮ መሆን", "አስተናጋጅ"],
        ["10፡45", "የመዝጊያ ቃል እና ለአስተናጋጁ ምስጋና", "መሪ"],
        ["11፡00", "ፕሮግራሙ ያበቃል", ""],
    ], [22, 108, 30]),
    ("n", "5.", "አንድ ጉዳይ እንዲወያይበት የሚፈልግ አባል ቢያንስ ከፕሮግራሙ አንድ ሳምንት በፊት ለጸሐፊው ይልካል። በዕለቱ "
                "የሚነሱ ጉዳዮች ጊዜ ካለ ብቻ ይሰማሉ።"),
    ("n", "6.", "ከ7፡00 እስከ 8፡40 ያለው መደበኛ ክፍል አጭርና ሥርዓት ያለው ይሆናል፤ ይህም አብዛኛው ጊዜ አብሮ ለመሆን "
                "እንዲውል ነው።"),

    ("h1", "አንቀጽ 4. ማስተናገድ"),
    ("n", "1.", "እያንዳንዱ ፕሮግራም በዕጣ በተወሰነው ቅደም ተከተል መሠረት ባገባ አባል በራሱ ቤት ይስተናገዳል።"),
    ("n", "2.", "ዕጣው በሁሉም አባላት ፊት አንድ ጊዜ ይወጣል፤ ጸሐፊው ሙሉውን ቅደም ተከተል ይመዘግባል። ይህ አንቀጽ "
                "ከሚፈቅደው በስተቀር ቅደም ተከተሉ አይቀየርም።"),
    ("n", "3.", "ሁለት አስተናጋጆች በስምምነት ተራቸውን መለዋወጥ ይችላሉ፤ ይህንንም ከፕሮግራሙ ቢያንስ አንድ ወር በፊት "
                "ለጸሐፊው ያሳውቃሉ።"),
    ("n", "4.", "በከባድ ምክንያት በተራው ማስተናገድ የማይችል አስተናጋጅ ቢያንስ አንድ ወር በፊት ለኮሚቴው ያሳውቃል። "
                "በቅደም ተከተሉ ቀጣዩ አስተናጋጅ ይተካል፤ ተራውን ያለፈው አባል በሚቀጥለው ጊዜ ያስተናግዳል።"),
    ("n", "5.", "ሁሉም ያገቡ አባላት አንድ ጊዜ ካስተናገዱ በኋላ ዑደቱ በተመሳሳይ ቅደም ተከተል እንደገና ይጀምራል። "
                "ከዕጣው በኋላ ያገቡ አባላት በቅደም ተከተሉ መጨረሻ ይጨመራሉ።"),
    ("n", "6.", "ያላገቡ አባላት ለማስተናገድ ወይም ካገባ አባል ጋር አብረው ለማስተናገድ በፈቃደኝነት መቅረብ ይችላሉ። "
                "ፈቃደኛው በሚቀጥለው ነጻ ተራ ላይ ይጨመራል።"),
    ("n", "7.", "አስተናጋጁ ቦታውን፣ ምግቡንና የቡና ሥነ ሥርዓቱን ያዘጋጃል፤ ከመሪው ጋር ፕሮግራሙን በሰዓቱ ያስኬዳል።"),
    ("n", "8.", "እንደ ልማዳችን የማስተናገድ ወጪ በአስተናጋጁ ይሸፈናል፤ ነገር ግን ማስተናገድ ውድድር አይደለም። ማንም "
                "አስተናጋጅ ከበፊተኛው ለመብለጥ ጫና እንዳይሰማው ስብሰባው ምክንያታዊ የወጪ መመሪያ ያወጣል። በምትኩ "
                "ስብሰባው ከገንዘቡ ቋሚ የማስተናገጃ ድጎማ ለመክፈል ሊወስን ይችላል።"),
    ("n", "9.", "በፕሮግራሙ መዝጊያ እያንዳንዱ አባል አስተናጋጁን ያመሰግናል፤ ማንም አባል የአስተናጋጁን ቤት ወይም ምግብ "
                "አይተችም።"),

    ("h1", "አንቀጽ 5. ኮሚቴው"),
    ("n", "1.", "ስብሰባው በአራት ሰዎች ኮሚቴ ይመራል፦ መሪ፣ ምክትል መሪ፣ ጸሐፊ እና ገንዘብ ያዥ።"),
    ("n", "2.", "ኃላፊነቶቻቸው፦"),
    ("b", "መሪ፦ ፕሮግራሙን ይመራል፣ ስብሰባውን ይወክላል፣ ሥርዓት ያስጠብቃል፣ ይህ ደንብ መከበሩን ያረጋግጣል።"),
    ("b", "ምክትል መሪ፦ መሪው በሌለበት ይተካል፤ ከእያንዳንዱ ፕሮግራም በፊት ከአስተናጋጁ ጋር ያስተባብራል።"),
    ("b", "ጸሐፊ፦ ቃለ ጉባኤ፣ የመገኘት መዝገብ፣ የማስተናገድ ቅደም ተከተል እና የቅጣት መዝገብ ይይዛል፤ ማስታወቂያና "
          "ማስታወሻ ይልካል።"),
    ("b", "ገንዘብ ያዥ፦ መዋጮና ቅጣት ይሰበስባል፣ የሂሳብ መዝገብና የባንክ ሂሳብ ይይዛል፣ በእያንዳንዱ ፕሮግራም ሪፖርት "
          "ያቀርባል።"),
    ("n", "3.", "ኮሚቴው በዓመቱ የመጀመሪያ ፕሮግራም ላይ በተገኙ አባላት አብላጫ ድምፅ ይመረጣል። እያንዳንዱ ለሁለት ዓመት "
                "ያገለግላል፤ በተከታታይ አንድ ጊዜ ብቻ እንደገና ሊመረጥ ይችላል። ከዚያ በኋላ ቢያንስ አንድ የሥራ ዘመን ያርፋል።"),
    ("n", "4.", "ዕዳ የሌለበት ማንኛውም አባል ለማንኛውም ቦታ መወዳደር ይችላል።"),
    ("n", "5.", "ስብሰባው የኮሚቴ አባልን በታማኝነት ጉድለት፣ በተደጋጋሚ መቅረት ወይም ኃላፊነትን በመዘንጋት ምክንያት፣ "
                "ከተሰማ በኋላ፣ በሁለት ሦስተኛ ድምፅ ሊያነሳው ይችላል።"),
    ("n", "6.", "አንድ ቦታ ክፍት ከሆነ ኮሚቴው እስከ ቀጣዩ ምርጫ ድረስ አንድ አባል ይሾማል።"),
    ("n", "7.", "የኮሚቴ አባላት ክፍያ አይከፈላቸውም፤ ከመዋጮም ከቅጣትም ነጻ አይደሉም።"),

    ("h1", "አንቀጽ 6. ገንዘብ"),
    ("n", "1.", "እያንዳንዱ አባል በየወሩ 700 ብር ያዋጣል። ክፍያው እስከ ወሩ 10ኛ ቀን ድረስ በስብሰባው የባንክ ሂሳብ ወይም "
                "ለገንዘብ ያዡ በደረሰኝ ይፈጸማል።"),
    ("n", "2.", "ስብሰባው በራሱ ስም አንድ የባንክ ሂሳብ ይይዛል። ገንዘብ ለማውጣት ሁለት ፊርማ ያስፈልጋል፦ የገንዘብ ያዡ እና "
                "የመሪው (ወይም የምክትል መሪው)።"),
    ("n", "3.", "ገንዘቡ የሚውለው ለሚከተሉት ብቻ ነው፦"),
    ("b", "ለአባል ሠርግ፣ ልደት፣ ከባድ ሕመም ወይም በቅርብ ቤተሰቡ ሞት ሲደርስ በድጋፍ ሠንጠረዡ በተወሰነው መጠን የሚሰጥ ድጋፍ፤"),
    ("b", "ችግር ላይ ላለ አባል በስብሰባው ፈቃድ የሚሰጥና በተስማሙበት ሁኔታ የሚመለስ የአስቸኳይ ጊዜ ብድር፤"),
    ("b", "የጋራ የቤተሰብ ዝግጅቶች እና የስብሰባው የራሱ ወጪዎች (የጽሕፈት መሣሪያ፣ ደረሰኝ፣ የባንክ ክፍያ)፤"),
    ("b", "በተገኙ አባላት ሁለት ሦስተኛ የጸደቀ ማንኛውም ሌላ ዓላማ።"),
    ("n", "4.", "የድጋፍ ሠንጠረዡ በስብሰባው ይወሰናል፤ በየዓመቱ ይገመገማል፦"),
    ("t", [
        ["ክስተት", "ከገንዘቡ የሚሰጥ ድጋፍ (ብር)"],
        ["የአባል ሠርግ", ""],
        ["የአባል ልጅ ልደት", ""],
        ["የአባል ወላጅ፣ ባል/ሚስት ወይም ልጅ ሞት", ""],
        ["የአባል ከባድ ሕመም ወይም ሆስፒታል መተኛት", ""],
    ], [100, 60]),
    ("n", "5.", "ያለ ጽሑፍ ጥያቄ፣ ያለ ገንዘብ ያዡ መዝገብ እና ያለ መሪው ፈቃድ ከገንዘቡ ምንም ክፍያ አይወጣም። ከሠንጠረዡ "
                "መጠን በላይ የሆኑ ክፍያዎች የስብሰባው ድምፅ ያስፈልጋቸዋል።"),
    ("n", "6.", "ገንዘብ ያዡ በእያንዳንዱ ፕሮግራም ሪፖርት ያቀርባል፦ የተሰበሰበ መዋጮ፣ የተሰበሰበ ቅጣት፣ የተከፈለ ክፍያ እና "
                "ቀሪ ሂሳብ። ሪፖርቱ በጽሑፍ ሆኖ ከቃለ ጉባኤው ጋር ይያያዛል።"),
    ("n", "7.", "የኮሚቴ አባል ያልሆኑ ሁለት አባላት በዓመት አንድ ጊዜ የሂሳብ መዝገቡንና የባንክ መግለጫውን መርምረው "
                "ለስብሰባው ሪፖርት ያደርጋሉ።"),
    ("n", "8.", "ከ30 ቀን በላይ የዘገየ መዋጮ በወር 100 ብር የመዘግየት ክፍያ ይኖረዋል።"),
    ("n", "9.", "ስብሰባው የመዋጮውን መጠን በሁለት ሦስተኛ ድምፅ መቀየር ይችላል። ለውጡ ከሚቀጥለው ሩብ ዓመት ጀምሮ "
                "ተግባራዊ ይሆናል።"),

    ("h1", "አንቀጽ 7. መገኘት እና ቅጣት"),
    ("n", "1.", "በእያንዳንዱ ፕሮግራም መገኘት የአባልነት ግዴታ ነው።"),
    ("n", "2.", "መገኘት የማይችል አባል ከፕሮግራሙ ቢያንስ ሦስት ቀን በፊት ለጸሐፊው ያሳውቃል።"),
    ("n", "3.", "ቅጣቶች እንደሚከተለው ናቸው፦"),
    ("t", [
        ["ሁኔታ", "ቅጣት (ብር)"],
        ["ሳያሳውቅ መቅረት", "2,000"],
        ["ቢያንስ 3 ቀን በፊት አሳውቆ መቅረት", "1,000"],
        ["በሚታለፍ ምክንያት መቅረት (ቁጥር 4 ይመልከቱ)", "የለም"],
        ["ሳያሳውቅ ከ30 ደቂቃ በላይ መዘግየት", "200"],
        ["ከመሪው አንድ ማስጠንቀቂያ በኋላ ፕሮግራሙን መረበሽ", "500"],
        ["አስተናጋጅ ያለ ከባድ ምክንያት ከአንድ ወር ባነሰ ማስታወቂያ ተራውን መሰረዝ", "1,000"],
    ], [130, 30]),
    ("n", "4.", "የሚታለፉ ምክንያቶች፦ የራስ ሕመም ወይም የባል፣ የሚስት ወይም የልጅ ሕመም፤ ሞት ወይም ቀብር፤ ልደት፤ የሥራ "
                "ጉዞ፤ ፈተና፤ እና አገራዊ ወይም ሃይማኖታዊ ግዴታ። ጸሐፊው ምክንያቱን ይመዘግባል። ኮሚቴው ሌሎች ከባድ "
                "ምክንያቶችን ሊቀበል ይችላል።"),
    ("n", "5.", "ከከተማ ውጭ ወይም በውጭ አገር የሚኖሩ አባላት ከመገኘት ነጻ ናቸው፤ በቪዲዮ ጥሪ መሳተፍ ይችላሉ። ስብሰባው "
                "የተለየ መጠን ካልተስማማ በስተቀር መዋጮ መክፈላቸውን ይቀጥላሉ።"),
    ("n", "6.", "ቅጣት በዕለቱ በጸሐፊው ይመዘገባል፤ በሚቀጥለው ፕሮግራም ይገለጻል። ከሚቀጥለው ፕሮግራም በፊት ወይም በዕለቱ "
                "ይከፈላል።"),
    ("n", "7.", "ቅጣትን የሚቃወም አባል በሁለት ሳምንት ውስጥ ለኮሚቴው ያቀርባል። ኮሚቴው ይወስናል፤ አባሉ በአንቀጽ 10 "
                "መሠረት ለሙሉ ስብሰባው ይግባኝ ማለት ይችላል።"),
    ("n", "8.", "ያልተከፈለ ቅጣት ያለበት አባል እስኪከፍል ድረስ ድምፅ አይሰጥም። ያልተከፈሉ ቅጣቶች በአንቀጽ 2 መሠረት "
                "እንደ ያልተከፈለ መዋጮ ይቆጠራሉ።"),
    ("n", "9.", "ቅጣቶች ወደ ገንዘቡ ይገባሉ፤ ከመዋጮ ጋር ሪፖርት ይደረጋሉ።"),

    ("h1", "አንቀጽ 8. የሥነ ምግባር ደንብ"),
    ("n", "1.", "እንደ ወንድማማችና እህትማማች እርስ በርስ በአክብሮት እንነጋገራለን። ስድብ፣ ጩኸት፣ ማሾፍ የለም።"),
    ("n", "2.", "የአስተናጋጁን ቤት እንደ ራሳችን እናከብራለን፦ በሰዓቱ እንደርሳለን፣ ስንጠየቅ እንረዳለን፣ ቦታውን እንዳገኘነው "
                "እንተዋለን።"),
    ("n", "3.", "በፕሮግራሙ መደበኛ ክፍል ስልኮች ድምፅ አልባ ይሆናሉ።"),
    ("n", "4.", "በፕሮግራሙ ጊዜ የፖለቲካና የንግድ ክርክር አይደረግም።"),
    ("n", "5.", "ወላጆች ለልጆቻቸው ባሕርይና ደኅንነት ኃላፊ ናቸው።"),
    ("n", "6.", "መጠጥ ከቀረበ በመጠን ይወሰዳል። ሥርዓት ያጣ አባል እንዲወጣ ይጠየቃል፤ በአንቀጽ 7 መሠረት ይቀጣል።"),
    ("n", "7.", "አንድ አባል በስብሰባው በሚስጥር ያካፈለው በቤተሰቡ ውስጥ ይቀራል።"),
    ("n", "8.", "በሌላ አባል ላይ ቅሬታ ያለው አባል በአንቀጽ 10 መሠረት ያቀርባል እንጂ በስብሰባው ፊት ወይም በማኅበራዊ ሚዲያ "
                "አያነሳም።"),
    ("n", "9.", "መሪው ለጥሰት አንድ ማስጠንቀቂያ ሊሰጥ ይችላል። በዚያው ፕሮግራም ሁለተኛ ጥሰት ይቀጣል። ተደጋጋሚ ጥሰት "
                "ለስብሰባው ይቀርባል፤ ስብሰባውም አባሉን ለአንድ ፕሮግራም ሊያግድ ይችላል።"),

    ("h1", "አንቀጽ 9. ውሳኔ እና ድምፅ አሰጣጥ"),
    ("n", "1.", "ስብሰባው በአጠቃላይ ይወስናል። ኮሚቴው ውሳኔዎችን ያስፈጽማል፤ ከዕለት ተዕለት ጉዳዮች በስተቀር ብቻውን "
                "አይወስንም።"),
    ("n", "2.", "ምልዓተ ጉባኤ፦ ውሳኔዎች የሚጸኑት ከአባላት ከግማሽ በላይ ሲገኙ ብቻ ነው።"),
    ("n", "3.", "መደበኛ ጉዳዮች በተገኙ አባላት አብላጫ ድምፅ ያልፋሉ። ድምፅ እኩል ከሆነ መሪው ይወስናል።"),
    ("n", "4.", "የሚከተሉት የተገኙ አባላት ሁለት ሦስተኛ ድምፅ ያስፈልጋቸዋል፦ የመዋጮ መጠን መቀየር፣ ቅጣት መቀየር፣ ከድጋፍ "
                "ሠንጠረዡ በላይ ማውጣት፣ አባልን ወይም የኮሚቴ አባልን ማገድ ወይም ማንሳት፣ እና ይህን ደንብ ማሻሻል።"),
    ("n", "5.", "ድምፅ በእጅ ማንሳት ይሰጣል። ማንኛውም ሦስት አባላት ሚስጥራዊ ድምፅ መጠየቅ ይችላሉ።"),
    ("n", "6.", "እያንዳንዱ አባል አንድ ድምፅ አለው። በውክልና ድምፅ መስጠት የለም፤ ነገር ግን በውጭ አገር ያለ አባል አስቀድሞ "
                "በታወቀ ጉዳይ ላይ በጽሑፍ ድምፅ መስጠት ይችላል።"),
    ("n", "7.", "የተወሰነ ጉዳይ አዲስ እውነታ ካልተገኘ በስተቀር ለአንድ ዓመት እንደገና አይነሳም።"),

    ("h1", "አንቀጽ 10. አለመግባባትን መፍታት"),
    ("n", "1.", "በማንኛውም ቤተሰብ አለመግባባት ይጠበቃል። ዋናው ነገር እንዴት እንደሚፈታ ነው።"),
    ("n", "2.", "ደረጃዎቹ በቅደም ተከተል፦"),
    ("b", "ደረጃ 1. ሁለቱ አባላት በግል ተነጋግረው በሁለት ሳምንት ውስጥ በራሳቸው ለመፍታት ይሞክራሉ።"),
    ("b", "ደረጃ 2. ካልተፈታ አንዱ አባል ለኮሚቴው በጽሑፍ ያቀርባል። ኮሚቴው ሁለቱንም በአንድ ወር ውስጥ ሰምቶ የመፍትሔ "
          "ሐሳብ ያቀርባል።"),
    ("b", "ደረጃ 3. አንዱ አባል የኮሚቴውን ሐሳብ ካልተቀበለ ጉዳዩ በሚቀጥለው ፕሮግራም ለሙሉ ስብሰባው ይቀርባል። ስብሰባው "
          "ሁለቱንም ሰምቶ በአብላጫ ድምፅ ይወስናል። ድምፅ በሚሰጥበት ጊዜ ሁለቱም አባላት ከክፍሉ ይወጣሉ።"),
    ("b", "ደረጃ 4. ክርክሩ የኮሚቴ አባልን የሚመለከት ከሆነ ወይም የስብሰባው ውሳኔ ተቀባይነት ካላገኘ፣ ጉዳዩ ስብሰባው "
          "ወደመረጠው የወላጆች ትውልድ ሽማግሌ ይሄዳል። የሽማግሌው ቃል የመጨረሻ ነው።"),
    ("n", "3.", "ምንም አለመግባባት በማኅበራዊ ሚዲያ ወይም ከቤተሰብ ውጭ ካሉ ሰዎች ጋር አይወያይም።"),
    ("n", "4.", "በእነዚህ ደረጃዎች ለመሳተፍ እምቢ የሚል ወይም የቤተሰብ አለመግባባትን ወደ ውጭ ሰዎች የሚወስድ አባል "
                "1,000 ብር ይቀጣል፤ ሊታገድም ይችላል።"),
    ("n", "5.", "አለመግባባት ሲፈታ ሁለቱ አባላት በስብሰባው ፊት እጅ ይጨባበጣሉ፤ ጉዳዩ ተዘግቶ ይመዘገባል።"),

    ("h1", "አንቀጽ 11. መዝገብ እና ግልጽነት"),
    ("n", "1.", "ጸሐፊው የአባላት መዝገብ፣ የመገኘት ዝርዝር፣ የእያንዳንዱ ፕሮግራም ቃለ ጉባኤ፣ የማስተናገድ ቅደም ተከተል "
                "እና የቅጣት መዝገብ ይይዛል።"),
    ("n", "2.", "ገንዘብ ያዡ የመዋጮ መዝገብ፣ ደረሰኞች፣ የባንክ መግለጫዎች እና የክፍያ መዝገብ ይይዛል።"),
    ("n", "3.", "ቃለ ጉባኤ በሚቀጥለው ፕሮግራም ተነቦ በአባላት ይጸድቃል።"),
    ("n", "4.", "ማንኛውም አባል በማንኛውም ጊዜ ማንኛውንም መዝገብ ለማየት መጠየቅ ይችላል፤ ኮሚቴው በአንድ ሳምንት ውስጥ "
                "ያሳያል።"),
    ("n", "5.", "መዝገቦች በጋራ ማኅደር፣ በወረቀትና በዲጂታል፣ ይቀመጣሉ፤ በእያንዳንዱ ምርጫ ለሚቀጥለው ኮሚቴ ይተላለፋሉ።"),
    ("n", "6.", "የዚህ ደንብ ቅጂ ለእያንዳንዱ አባል እና ለእያንዳንዱ አዲስ አባል ሲቀላቀል ይሰጣል።"),

    ("h1", "አንቀጽ 12. ማሻሻያ እና ማጽደቅ"),
    ("n", "1.", "ማንኛውም አባል ማሻሻያ በጽሑፍ ለጸሐፊው ማቅረብ ይችላል። ሐሳቡ በአንድ ፕሮግራም ይገለጻል፤ በሚቀጥለው "
                "ድምፅ ይሰጥበታል፤ ይህም እያንዳንዱ አባል ለማሰብ ሦስት ወር እንዲኖረው ነው።"),
    ("n", "2.", "ማሻሻያ በተገኙ አባላት ሁለት ሦስተኛ ድምፅ ያልፋል፤ ከሚቀጥለው ፕሮግራም ጀምሮ ተግባራዊ ይሆናል።"),
    ("n", "3.", "ይህ ደንብ የሚጸድቀው በአንድ ፕሮግራም ሙሉ በሙሉ ተነቦ፣ ከሁሉም አባላት ሁለት ሦስተኛ ሲያጸድቁት እና "
                "በኮሚቴውና በተገኙ አባላት ሲፈረም ነው።"),
    ("n", "4.", "ስብሰባው ሲያጸድቅ መወሰን ያለበት ጉዳዮች፦"),
    ("b", "የማስተናገድ የወጪ መመሪያ ወይም ድጎማ (አንቀጽ 4፣ ቁጥር 8)፤"),
    ("b", "የድጋፍ ሠንጠረዥ መጠኖች (አንቀጽ 6፣ ቁጥር 4)፤"),
    ("b", "ባልና ሚስት ድምፅ ይስጡ አይስጡ (አንቀጽ 2፣ ቁጥር 2)፤"),
    ("b", "በውጭ አገር ላሉ አባላት መዋጮ (አንቀጽ 7፣ ቁጥር 5)፤"),
    ("b", "ለመጨረሻ ይግባኝ የሚሆን ሽማግሌ (አንቀጽ 10)።"),
    ("sig", {
        "title": "ማጽደቅ እና ፊርማ",
        "line": "የጸደቀበት ቀን ____________________ ቦታ ____________________።",
        "cols": ["ኃላፊነት", "ስም", "ፊርማ"],
        "posts": ["መሪ", "ምክትል መሪ", "ጸሐፊ", "ገንዘብ ያዥ"],
        "members": "የተገኙ አባላት",
        "mcols": ["ተ.ቁ.", "ስም", "ፊርማ"],
    }),
]


# --------------------------------------------------------------------------
# STYLES AND BUILDER
# --------------------------------------------------------------------------
INK = colors.HexColor("#1f2933")
RULE = colors.HexColor("#9aa5b1")
TINT = colors.HexColor("#eef2f6")


def make_styles(font, bold):
    base = ParagraphStyle("base", fontName=font, fontSize=10.5, leading=15, textColor=INK)
    return {
        "title": ParagraphStyle("title", parent=base, fontName=bold, fontSize=24, leading=30,
                                alignment=TA_CENTER, spaceAfter=6),
        "subtitle": ParagraphStyle("subtitle", parent=base, fontSize=13, leading=18,
                                   alignment=TA_CENTER, textColor=colors.HexColor("#52606d")),
        "part": ParagraphStyle("part", parent=base, fontName=bold, fontSize=18, leading=24,
                               spaceAfter=12),
        "h1": ParagraphStyle("h1", parent=base, fontName=bold, fontSize=13.5, leading=18,
                             spaceBefore=14, spaceAfter=6, keepWithNext=1),
        "p": ParagraphStyle("p", parent=base, spaceAfter=6),
        "n": ParagraphStyle("n", parent=base, leftIndent=9 * mm, firstLineIndent=-9 * mm, spaceAfter=4),
        "b": ParagraphStyle("b", parent=base, leftIndent=17 * mm, firstLineIndent=-5 * mm, spaceAfter=3),
        "cell": ParagraphStyle("cell", parent=base, fontSize=10, leading=13),
        "cellh": ParagraphStyle("cellh", parent=base, fontName=bold, fontSize=10, leading=13),
    }


def table(rows, widths, st):
    data = [[Paragraph(c, st["cellh"] if r == 0 else st["cell"]) for c in row]
            for r, row in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TINT),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, RULE),
        ("LINEBELOW", (0, 1), (-1, -1), 0.3, RULE),
        ("BOX", (0, 0), (-1, -1), 0.6, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def signature_block(spec, st):
    out = [Spacer(1, 10), Paragraph(spec["title"], st["h1"]), Paragraph(spec["line"], st["p"]), Spacer(1, 6)]
    rows = [spec["cols"]] + [[p, "", ""] for p in spec["posts"]]
    out.append(table(rows, [40, 70, 50], st))
    out.append(Spacer(1, 10))
    rows = [spec["mcols"]] + [[str(i), "", ""] for i in range(1, 21)]
    # Keep the members list on one page rather than splitting it.
    out.append(KeepTogether([Paragraph(spec["members"], st["p"]), table(rows, [16, 94, 50], st)]))
    return out


def render(content, st):
    story = []
    for item in content:
        kind = item[0]
        if kind == "h1":
            story.append(Paragraph(item[1], st["h1"]))
        elif kind == "p":
            story.append(Paragraph(item[1], st["p"]))
        elif kind == "n":
            story.append(Paragraph(f"{item[1]}&nbsp;&nbsp;{item[2]}", st["n"]))
        elif kind == "b":
            story.append(Paragraph(f"•&nbsp;&nbsp;{item[1]}", st["b"]))
        elif kind == "t":
            story.append(Spacer(1, 4))
            story.append(table(item[1], item[2], st))
            story.append(Spacer(1, 8))
        elif kind == "sig":
            story.extend(signature_block(item[1], st))
        elif kind == "pagebreak":
            story.append(PageBreak())
    return story


def page_decor(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(colors.HexColor("#52606d"))
    canvas.drawString(20 * mm, 12 * mm, "Asefa Family Gathering Constitution")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, f"Page {doc.page}")
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.4)
    canvas.line(20 * mm, 16 * mm, A4[0] - 20 * mm, 16 * mm)
    canvas.restoreState()


def build():
    en = make_styles("Helvetica", "Helvetica-Bold")
    am = make_styles("Kefa", "Kefa")

    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=20 * mm, bottomMargin=24 * mm,
                            title="Asefa Family Gathering Constitution",
                            author="The Asefa Family Gathering")

    story = []
    # Cover
    story += [
        Spacer(1, 70 * mm),
        Paragraph("Asefa Family Gathering", en["title"]),
        Paragraph("Constitution and Rules", en["subtitle"]),
        Spacer(1, 10 * mm),
        Paragraph("የአሰፋ ቤተሰብ ስብሰባ", ParagraphStyle("t2", parent=am["title"], fontSize=22)),
        Paragraph("መተዳደሪያ ደንብ", am["subtitle"]),
        Spacer(1, 30 * mm),
        Paragraph(f"Draft for adoption &middot; {DATE_EN}", en["subtitle"]),
        Paragraph(f"ለማጽደቅ የቀረበ ረቂቅ &middot; {DATE_AM}", am["subtitle"]),
        PageBreak(),
    ]
    # English part
    story.append(Paragraph("Part A &middot; English", en["part"]))
    story += render(CONTENT_EN, en)
    story.append(PageBreak())
    # Amharic part
    story.append(Paragraph("ክፍል ለ · አማርኛ", am["part"]))
    story += render(CONTENT_AM, am)

    doc.build(story, onFirstPage=lambda c, d: None, onLaterPages=page_decor)
    print("Wrote", OUT)


if __name__ == "__main__":
    build()
