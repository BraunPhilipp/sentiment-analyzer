DATABASES
=========

```

mysql -u root -p

CREATE DATABASE wenti_db;
USE wenti_db;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE TABLE IF NOT EXISTS `wt_reviews` (
`ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `review_text` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `review_category` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'en',
  `review_score` bigint(20) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (ID)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `wt_tracker` (
`ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `keyword` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `volume` bigint(20) unsigned NOT NULL DEFAULT '0',
  `min_id` bigint(20) unsigned NOT NULL DEFAULT '0',
  `max_id` bigint(20) unsigned NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_at` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (ID)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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
  `tweet_keyword` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (ID)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `wt_tweet_volume` (
`ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `keyword` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `volume` bigint(20) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (ID)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `wt_tweet_sentiment` (
`ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `keyword` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `sentiment` bigint(20) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (ID)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

```
