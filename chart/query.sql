use honr3310;

select mode, avg(negative_emotions), avg(positive_emotions), count(*)
from Song
where title not in
('And I Love Her', 'Another Girl', 'Being for the Benefit of Mr. Kite!', 'Birthday', 'Cry Baby Cry', 'Doctor Robert', 'Drive My Car', 'Fixing A Hole', 'For No One', 'For You Blue', 'Good Day Sunshine', 'Happiness is A Warm Gun', 'Here, There and Everywhere', 'Hey Bulldog', 'I Me Mine', "I Want You (She's So Heavy)", "I'll Be Back", "I'm Happy Just To Dance With You", 'If I Fell', 'Lovely Rita', 'Lucy In The Sky With Diamonds', 'Martha My Dear', "Octopus's Garden", 'Only A Northern Song', 'Penny Lane', 'Piggies', 'Savoy Truffle', "Sgt. Pepper's Lonely Hearts Club Band (Reprise)", 'Something', 'Strawberry Fields Forever', 'Sun King', 'The End', 'The Fool On The Hill', 'Things We Said Today', 'We Can Work It Out', 'Not a Second Time', 'While My Guitar Gently Weeps', 'You Never Give Me Your Money', "You're Going to Lose That Girl", 'Your Mother Should Know')
group by 1;

select avg(negative_emotions), avg(positive_emotions)
from Song
where title not in
('And I Love Her', 'Another Girl', 'Being for the Benefit of Mr. Kite!', 'Birthday', 'Cry Baby Cry', 'Doctor Robert', 'Drive My Car', 'Fixing A Hole', 'For No One', 'For You Blue', 'Good Day Sunshine', 'Happiness is A Warm Gun', 'Here, There and Everywhere', 'Hey Bulldog', 'I Me Mine', "I Want You (She's So Heavy)", "I'll Be Back", "I'm Happy Just To Dance With You", 'If I Fell', 'Lovely Rita', 'Lucy In The Sky With Diamonds', 'Martha My Dear', "Octopus's Garden", 'Only A Northern Song', 'Penny Lane', 'Piggies', 'Savoy Truffle', "Sgt. Pepper's Lonely Hearts Club Band (Reprise)", 'Something', 'Strawberry Fields Forever', 'Sun King', 'The End', 'The Fool On The Hill', 'Things We Said Today', 'We Can Work It Out', 'Not a Second Time', 'While My Guitar Gently Weeps', 'You Never Give Me Your Money', "You're Going to Lose That Girl", 'Your Mother Should Know');