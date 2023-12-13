Dependencies:
    - There are no specific dependencies needed to run the code. All of the nessecary libraries are imported at the tip of the code. The Librosa library is not actually used, so is not nessecary to install

Limititations:
    - There are certain inputs that will crash the code. Specfically, if you enter a city that is not listed on OpenWeathermap.org, or you don't enter a city at all (or enter it with a typo) the code will give you an error

Explanation:
    - There are really no specific things needed to run the code. Just enter the city that you're currently in, and the code should return a reccommneded song. The CSV file with all of the songs is also in the gitrepo, in theory it would be nice if it could return things from your personal music library, but that bit will hopefully be coming soon as I want to get the apple music api authentication eventually