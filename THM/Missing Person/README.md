# Missing Person — OSINT Write-Up

## Challenge Overview

This challenge requires the use of Open-Source Intelligence (OSINT) techniques to assist in locating a missing person. Two images are provided:

- `food.jpg`
- `MotoGP.jpg`

The objective is to analyze the images, extract relevant information, and pivot through publicly available sources to answer a series of questions.

---

## Question 1: What is the commercial name of this circuit?

Perform a reverse image search on `MotoGP.jpg` using Google Images or a similar service. The circuit can be identified immediately from the search results.

**Technique used:** Reverse image search

---

## Question 2: When did the event take place?

Extract the image metadata using:

```bash
exiftool MotoGP.jpg
```

The metadata reveals the date the photograph was taken. Once the circuit has been identified, search for the MotoGP event that took place at that location on the recorded date. The event information will provide the full date range required by the challenge.

**Technique used:** Metadata analysis + event correlation

---

## Question 3: He told me he ate delicious Mexican food. What is the name of the restaurant?

Perform a reverse image search on `food.jpg`. The restaurant can be identified directly from the search results and associated online content.

**Technique used:** Reverse image search

---

## Question 4: At what time was this photo taken?

Use ExifTool to inspect the image metadata:

```bash
exiftool food.jpg
```

The timestamp stored in the EXIF data contains the exact time the photograph was captured.

**Technique used:** Metadata analysis

---

## Question 5: He sent me a message, this is the last I heard from him:

> "Went to this cool MotoGP after party, and became friends with one of the local DJs who played that night. We're going to visit a cave tomorrow."

### What is the full address of the bar's location?

Search for terms related to the MotoGP afterparty, such as:

```text
2025 MotoGP bar afterparty Indonesia
```

By identifying the venue that hosted the event, you can obtain the complete address from its social media pages or business listings.

**Technique used:** Event research + social media investigation

---

## Question 6: What is the DJ's stage name?

After locating the bar, review its social media content, particularly Facebook posts, reels, and event promotions. The DJ's stage name is mentioned in one of the event-related posts.

**Technique used:** Social media analysis

---

## Question 7: After digging into the DJ's other online accounts, what cave does he take tourists to?

Search for the DJ's stage name on Facebook. One of the DJ's profiles advertises local tours and mentions the cave visited with tourists.

Example search:

```text
<DJ Name> Facebook
```

The cave name can be found in the tour-related content.

**Technique used:** Account pivoting

---

## Question 8: What number did the DJ list for his tour business?

Continue reviewing the DJ's tour-related Facebook page. The contact number is publicly listed in the business information section.

**Technique used:** Social media intelligence (SOCMINT)

---

## Summary

This challenge combines several common OSINT techniques:

- Reverse image searching
- Metadata extraction with ExifTool
- Event correlation
- Social media analysis
- Account pivoting
- Business information gathering

The investigation demonstrates how seemingly unrelated pieces of public information can be combined to reconstruct an individual's movements and associations.
