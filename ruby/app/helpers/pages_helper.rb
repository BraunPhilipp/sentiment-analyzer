module PagesHelper

  def num_keywords
    Tracker.count
  end

  def num_reviews
    Review.count
  end

  def num_tweets
    TweetDatum.count
  end

  def current_keywords
    Tracker.all
  end

end
