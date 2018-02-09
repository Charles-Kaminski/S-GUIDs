
# S-GUIDs (Simple Globally Unique IDs)
Charles Kaminski, 2015. Updated for release, 2018.
## Introduction
The Simple Globally Unique Ids described below have been engineered specifically for the needs of LexisNexis Risk Solutions for use in our multitude of products and systems around the globe.  Their intended use is for both customer-facing transaction IDs as well as for internal subsystem tracking ID’s.  

These IDs are: 
 - Globally unique, comparatively compact, and high-performing (meaning there is little burden to create them on demand).  
 - Quasi-sequential by design so as to realize maximum performance when inserting into indexes.  They will not materially fragment or otherwise degrade write-cached indexes that store them.
 - Minimally  complex.  Simple to create.  Simple to expand.
 - Free from architectural dependencies.  They can be created on state-full and stateless subsystems alike and do not require seeds or other forms of state-coordination so long as the subsystem can access reasonably accurate time.
 - Easily implementable within new acquisitions without concern for hidden dependencies or hardware conflicts such as overlapping IP addresses or spoofed MAC ids – a concern with some standards.
 - Consistently implemented – a concern with some
   standards.

In a global multi-product ordering environment (MPO), a single request into one infrastructure could be on behalf of multiple customers and represent multiple product calls for each customer.  As such, a single MPO request can touch hundreds or thousands of subsystems in parallel.  S-GUIDs allow all of those Subsystem calls to be pieced together for a complete view of a transaction.  S-GUIDs enable the entire enterprise to be monitored and tracked from local command centers or a single command center.

S-GUIDs can be implemented in areas of the architecture previously not considered; such as on client machines and mobile devices; from within networking hardware; or even appended by advanced delivery networks prior to a transaction reaching a datacenter. 

The specific implementation described below supports a sustained 100 billion transactions a minute across the enterprise and supports bursts far greater than this.  100 billion sustained transactions a minute is the same as 525 quadrillion or 525 million billion transactions a year.  As a comparison, Visa Inc. executed [141 billion total transactions in all of 2016](https://usa.visa.com/dam/VCOM/global/about-visa/documents/visa-facts-figures-jan-2017.pdf).  As inconceivable as it is now, if the enterprise were to grow past 525 quadrillion transactions a year, S-GUIDs are trivial to extend given the framework below.

## Implementation

LexisNexis Risk Solutions teams should link to existing code held in a central repository on Github to generate S-GUIDs.  If code is not available for your specific programming language or system, it will be created for you.  For external teams, the repository will be made publicly accessible to the benefit of our customers and the broader computing community.  Scripts and code are included to assist engineers and product support specialists working with S-GUIDs.  This includes a number of capabilities such as the ability to extract the time component from an ID; the ability to encode or decode IDs from their binary and human-readable formats; as well as the ability to create a range of IDs to search for based on date/time ranges (a useful tool when you don’t know what you’re looking for).

### Composition

Size: Byte [16]

![Byte Layout](http://example.com/bytelayout.png) 

**Time Component** – Number of milliseconds since the UNIX epoch (January 1st, 1970).

**Random Component** – Random data is pulled from a source present on modern operating systems.  Random data comes from /dev/urandom on Linux-based and UNIX-based systems.  For Windows systems, the Microsoft Cryptographic API is used.  Certain programming languages will use these interfaces under the covers.

### Algorithm Pseudocode

1.	Allocate 16 bytes of memory for the S-GUID.
2.	Get the number of milliseconds since the UNIX epoch (January 1st, 1970) in an 8 byte unsigned long variable.  Note that this is not based on local time.  A good clue you have the correct value is if you change the time zone and the value does not change.
	1.	Example: Current milliseconds since epoch – 1469729511910
	1.	Time Component: 0000 0000 0000 0000 0000 0001 0101 0110 0011 0010 1011 0100 1001 1001 1110 0110
1.	Copy the last 5 bytes in step 2 into the first 5 bytes of the Global Transaction ID
1.	Get 11 bytes of random data seeded from the entropy pool present on all modern operating systems.  See “Random Component” above.
1.	Copy the 11 bytes of random data from step 4 into the last 11 bytes for the S-GUID.
1.	Return the allocated 16 byte variable from step 1 as the binary form of the S-GUID.

The binary form can be used internally for compactness and performance. On most systems, the preferred binary form is 16 bytes of contiguous data.  On some systems it may be easier to internally represent the binary form of the Global Transaction ID as 2 unsigned long longs of 8 bytes each.

### Encoding Scheme

Base58 encoding is implemented for readability and customer facing solutions.  Base58 encoding is used to balance compactness as well as readability.  Certain confusing characters have been removed out of the standard Base58 encoding scheme.  As such, Base58 includes all alphanumeric characters except for "0", "I", "O", and "l".  This can be confusing to see in print.  See the next line to understand what characters are included.

    static const char* pszBase58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";

### Examples of encoded S-GUIDs

Size: String [22]

6HUwe9WK1Nux9CFbecK1BU

6HUwe9XZxb3b88NjmsmfkR

### Considerations

**Operating System** - A healthy entropy pool is required and can be checked with simple system health scripts at system startup. 

**Docker Containers** – Some configurations of Docker may not allow the container to access the entropy pool maintained by the operating system.  This is a well-known issue with known workarounds as it affects containerized applications that require cryptographically secure random data (such as secure web applications).   Test your configuration to ensure this is not an issue for you.  

**Clock** – The operating system need only keep time to a limited degree of accuracy.  This is usually not an issue for modern computers. 

**Repeating Cycle** – The 5-byte time component allows for a 35-year repeating cycle.  This does not mean that you will get duplicates in 35 year or in 100 years.  It does mean that when archiving logs, you will want to keep a date-time stamp in the log entry.  This should already be best practices.

**Batch Jobs** – For LexisNexis Risk Solutions employees, please have your architect or tech lead reach out to me for a brief review of your batch use case.  For all others, read on.  

Extremely large and numerous batch jobs could exceed an enterprise limit of S-GUID assignment if your architecture were to assigning all of the S-GUIDs in your batches in a single millisecond of your batch jobs.  If a similar situation applies to you, then there are two solutions to this problem.  
1.	Extend the length of the random component of the S-GUID using the math below.
1.	Modify, in descending order, the time component of the S-GUIDs assigned in the batch job.  This would be based on an estimate of some minimum amount of time your batch will run given the number of transactions in your batch.  The first S-GUID’s value would be as if it was assigned at the start of the batch job.  The last S-GUID’s value would be as if it was assigned at the end of the batch job.   

## Criticisms

### Random Data

S-GUIDs depends on random data.  One of the criticism I often hear is that computers don’t produce random data and we have no way of properly seeding our algorithms with random data without specialized hardware.  This was true once that most computers could not produce truly random data and their quasi-random algorithms, if not seeded properly, could wreak havoc with this scheme.  This is no longer true with today’s modern operating systems.  Modern operating systems use a number of techniques, including system “noise”, to generate truly random data for cryptographic uses. 

### “So you’re telling me there’s a chance”

This is the criticism I hear most often, so I'm going go into a bit more detail here.  Also, linked here is an entertaining 2 minute video on [the challenges of communicating probabilities](https://www.youtube.com/watch?v=-3QldN3EnBI). 

The math quantifies the non-zero probability, no matter how small, there will be a collision; meaning two identical S-GUIDs will be generated.  The math here isn’t telling us to worry.  It’s telling us not to worry.

I have a great presentation on really big and really small numbers that helps here, but I’ll try to summarize it in the next few paragraphs.  

Take a handful of sand and think for a moment about how many grains of sand are in your hand.  There are roughly 10^5 grains of sand in a handful of sand (that’s a 1 with 5 zeros).  Look at the whole beach and think about how many grains of sand there are on the whole beach.  Think about all the beaches on the Earth and about how many grains of sand there must be.  It’s a lot.  There are about 10^18 grains of sand on the earth.  Now think about the vast cosmos and don’t count grains of sand but instead count something much smaller; Count atoms.  Count the number of atoms in the whole visible universe.  Think about all the people, cities, planets, solar systems, and galaxies (2 trillion of them).  Think about the whole visible universe.  Everything that humans will ever see or ever can see with our human eyes.  There are about 10^80 atoms in the visible universe (plus or minus a few orders magnitude).  All of these numbers seem close together and approachable because their exponents don’t seem very far apart.  But in reality they are very very far apart.  As in “size of the known universe” far apart.  It only takes a moment to grab a handful of sand and look up to the heavens on a starry night to realize this.  

Similarly, very small probabilities like 10^-5, 10^-18 and 10^-80 are also very “far” apart in their meaning.  So let’s take a two-paragraph journey in the opposite direction.

Math (with a little thermal dynamics sprinkled in) will allow us to calculate the non-zero probability that a carbon atom on a diamond will escape its crystal latus at room temperature.  It will also tell us the non-zero probability that 2 or 3 carbon atoms will escape before your eyes.  So, the “non-zero probability”, no matter how small, that a whole diamond will evaporate in front of your eyes must exist. 

Also, math will allow us to calculate the probability that some small portion of radioactive material (such as Uranium or Plutonium) will decay in the same instant.  And to take that non-zero probability to its absurdity, there must be some “non-zero probability” that all of it will instantaneously decay.

The reality is that these infinitesimally small probabilities, correctly interpreted, are confirming what you already know.  You will not see diamonds evaporate before your eyes at room temperature, naturally occurring radioactive minerals are quite safe from spontaneous detonation, and in the same vein, I am not worried about collisions of 128 bit S-GUIDs when executed at a rate below 100 billion per minute.  We continue to use S-GUIDs with great success and no issues.

## The Math

The math below (similarly represented in the file S-GUID_Probability_Calculations.ipynb) is broken down into two sections.  First I calculate the probability that a single collision will occur in any single millisecond.  Then I apply that probability over and over again for every millisecond across a particular time frame.  Think of it like this, what’s the probability you will win at BINGO?  Now what’s the probability you will win if you play again and again?  They are different.  The second calculation below accounts for the fact you are playing a game of BINGO you can never hope to win again and again.

### Probability of 1 collision in a millisecond

p1 = probability of 1 collision in 1 millisecond.  Milliseconds is chosen here because the time component of the S-GUID ensures uniqueness across a millisecond.  

k = number of transactions in a millisecond

b = number of bits of random data

e = Euler’s number

p1 = 1 – e^(-k * (k-1)/(2 * 2^b))

### Probability of 1 collision over a period of time

p = probability of 1 collision over a period of time

T = number of milliseconds in a given timeframe 

There are 3.1536 * 10^10 milliseconds in a year.

p = 1 – ((1 – p1)^T)

### Results

For 88 bits of random data, the following holds:

|Transactions/Minute|Transactions/Year|p1|p (T=35 years)
|--|--|--|--|
|1E6|5.26E11|3.88E-25|4.28E-13|
|1E7|5.26E12|4.43E-23|4.89E-11|
|1E8|5.26E13|4.48E-21|4.94E-09|
|1E9|5.26E14|4.49E-19|4.96E-07|
|1E10|5.26E15|4.49E-17|4.96E-05|
|1E11|5.26E16|4.49E-15|4.94E-03|

For 96 bits of random data (an expansion of 8 bits), the following holds:

|Transactions/Minute|Transactions/Year|p1|p (T=35 years)
|--|--|--|--|
|1E6|5.26E11|1.51E-27|1.67E-15|
|1E7|5.26E12|1.73E-25|1.91E-13|
|1E8|5.26E13|1.75E-23|1.93E-11|
|1E9|5.26E14|1.75E-21|1.93E-09|
|1E10|5.26E15|1.75E-19|1.93E-07|
|1E11|5.26E16|1.75E-17|1.93E-05|
|***1E12***|***5.26E17***|***1.75E-15***|***1.93E-03***|

## Real World Performance

The file S-GUID_Analysis.ipynb in the GitHub repository summarizes the initial study of S-GUIDs generated in a production system.  It shows that predictions match near perfectly with the real world environment.

## Conclusion

With the framework above in place, it is trivial to extend (or even shrink) S-GUIDs to any transaction count.  The reality is that even the largest enterprises have transaction counts well below 525 quadrillion transactions a year (that’s 525 million billion).  This means that 88 bits of random data will more than suffice.  With the time component, S-GUIDs fit nicely into 16 bytes or two unsigned long longs.
