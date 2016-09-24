class Api::TweetDatumsController < Api::ApiController

  before_filter :admin_access

  def index
    render json: TweetDatum.all
  end

  def search
    key = Tracker.where(:keyword => params[:q]).first
    tweets = TweetDatum.where(:tracker_id => key.id)

    render json: tweets
  end

  def create
    new_tweets = json_params

    new_tweets.each do |tw|
      if TweetDatum.where(:tweet_id => tw[:tweet_id]).empty?
        list = TweetDatum.new(tw)
        if !list.save
          render status: 422, json: {
            message: "Could not add a new tweet!",
            tweet: list
          }.to_json and return
        end
      end
    end

    render status: 200, json: {
      message: "Tweets were added to Database"
    }.to_json
  end

  private

    def json_params
      params.permit(:data => [:tweet_id, :tweet_date, :tweet_text, :tweet_lang, :tweet_retweet_count, :tweet_favorite_count, :tweet_user_id, :tweet_user_verified, :tweet_sentiment, :tweet_score, :tracker_id]).require(:data)
    end

    def admin_access
      head :unauthorized unless Rails.application.secrets.api_key == params[:api_key]
    end

end
