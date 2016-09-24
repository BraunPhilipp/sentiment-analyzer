##Twitter Sentiment Analyzer

###Outline
The provided code can be used to analyze tweet sentiment based on various keywords in realtime. Tweets are scored using basic Bayesian Classifier. The underlying dataset is based on various reviews from Amazon and Walmart. Therefore, the tool is easily adjustable for multilingual analysis.

###Module Structure
```
/api - Access to Ruby on Rails API
/doc - Documents related to the project
/logger - Logs various errors to error.log
/mysql - Direct Mysql Database Access
/reviews - Collects Reviews from Amazon and Walmart
/ruby - Ruby on Rails API
/sentiment - Analyzes Sentiment based on existing reviews
/twitter - Collects tweets using REST and Realtime API

main.py - Bundled Functions
sentiment.sh - Sentiment Analyzer
tweets.sh - Tweet Collector
```
###Tools
The Twitter Sentiment Classifier is powered using Python and Ruby on Rails. Tweets are collected using Twitter's REST API ( _TWITTER MODULE_ ). These tweets are then scored based on already collected reviews in the database ( _REVIEWS MODULE_ ). The exchange between the database and Python code is handled using a Ruby on Rails REST API ( _API MODULE_ ). Direct access to the MYSQL Server is also possible using the _MYSQL MODULE_. Further libraries such as NLTK are used to improve performance as well as accuracy of the analyzer.

###Bayesian Classifier
```
P( WORD | POSITIVE ) = ( WORD OCCURENCE IN POSITIVE SET + 1 ) / ( ALL POSITIVE WORDS )
```
_Reduce significant words > 10 in data set to speedup the algorithm. Remove pronouns and neutral nouns._
```
P( POSTIVE SENTENCE ) = P( POSITIVE NORMALIZED ) * P( WORD1 | POSTIVE ) * P( WORD2 | POSITIVE ) * ...
```
_To find word data quickly words could be stored in a dictionary._

###Filtering
Because of Twitter's open platform the amount of spam is extremely high. The amount of useful tweets can be increased using certain rules such as removing tweets containing @, ?, $, or tweets in a different language.

###Setup
**Install Ruby on Rails**

https://www.digitalocean.com/community/tutorials/how-to-deploy-a-rails-app-with-passenger-and-nginx-on-ubuntu-14-04

**MYSQL Installation**
```
mysql> SHOW DATABASES;
mysql> CREATE DATABASE database name;
mysql> DROP DATABASE database name;
mysql> USE events;
mysql> SHOW tables;
mysql> DESCRIBE potluck;
mysql> ALTER TABLE potluck ADD email VARCHAR(40) AFTER name;
```
**Enable Remote Access MYSQL**
```
sudo apt-get update
sudo apt-get install mysql-server

nano /etc/mysql/my.cnf

#skip-external-locking
#bind-address = 127.0.0.1
bind-address       = 0.0.0.0

mysql -p
use mysql;
UPDATE user SET password=PASSWORD('abcdef') WHERE user = 'root';
GRANT ALL PRIVILEGES ON *.* TO root@'%' IDENTIFIED BY 'abcdef';
FLUSH PRIVILEGES;
exit;

sudo ufw allow 3306
sudo service mysql restart
```
**Testing**
```
ssh root@IP_ADDRESS
ssh-keygen -R IP_ADDRESS
```
**Python Installation**
```
sudo apt-get install python3

sudo apt-get install python3-numpy
sudo apt-get install python3-pandas

sudo apt-get install python3-pip
sudo pip3 install PyMySQL
sudo pip3 install nltk

sudo apt-get install build-essential python3-dev python3-setuptools python3-numpy python3-scipy libatlas-dev libatlas3gf-base
sudo pip3 install scikit-learn

python3
import nltk
nltk.download('all')
nltk.download('maxent_treebank_pos_tagger');
nltk.download('averaged_perceptron_tagger')
```

**Run Tweet Harvester**
```
scp * root@IP_ADDRESS:~/

/etc/init/harvest.conf (edit as root)

start on runlevel [2345]
stop on runlevel [016]
respawn
exec python /path/to/your/COMPRESS.py

sudo start harvest

nohup sh spawn.sh &

ps -ef |grep nohup
kill -9 PID
```

**Database Installation**
```
mysql

mysql -u root -p

CREATE DATABASE wenti_db;
USE wenti_db;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE TABLE IF NOT EXISTS `wt_tweet_data` (
`ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `tweet_id` bigint(20) unsigned NOT NULL DEFAULT '0',
  `tweet_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `tweet_text` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `tweet_lang` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'en',
  `tweet_retweet_count` bigint(20) unsigned NOT NULL DEFAULT '0',
  `tweet_favorite_count` bigint(20) unsigned NOT NULL DEFAULT '0',
  `tweet_user_id` bigint(20) unsigned NOT NULL DEFAULT '0',
  `tweet_user_verified` bigint(20) unsigned NOT NULL DEFAULT '0',
  `tweet_sentiment` bigint(20) unsigned NOT NULL DEFAULT '0',
  `tweet_score` bigint(20) unsigned NOT NULL DEFAULT '0',
  `tweet_query` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (ID)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `wt_ratings` (
`ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `rating_text` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `rating_lang` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'en',
  `rating_score` bigint(20) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (ID)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `wt_tracker` (
`ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `query` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `volume` bigint(20) unsigned NOT NULL DEFAULT '0',
  `min_id` bigint(20) unsigned NOT NULL DEFAULT '0',
  `max_id` bigint(20) unsigned NOT NULL DEFAULT '0',
  `first_check` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `last_check` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (ID)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `wt_volume` (
`ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `query` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `volume` bigint(20) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (ID)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `wt_sentiment` (
`ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `query` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `sentiment` bigint(20) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (ID)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Additional Notes**
```
git clone https://username@github.com/*****/******.git
rvmsudo rails server -p 80
```
