class Api::TweetSentimentsController < Api::ApiController

  before_filter :admin_access

  def index
    render json: TweetSentiment.all
  end

  def create
    key = Tracker.where(:keyword => params[:keyword]).first
    list = TweetSentiment.new(:tracker_id => key.id, :date => params[:date], :sentiment => params[:sentiment])

    if !list.save
      render status: 422, json: {
        message: "Failed to create Tweet Sentiment",
        tweet: list
      }.to_json and return
    end

    render status: 200, json: {
      message: "Successfully created Tweet Sentiment"
    }.to_json
  end

  def delete
    key = Tracker.where(:keyword => params[:keyword]).first
    if TweetSentiment.exists?(:tracker_id => key.id, :date => params[:date])
      list = TweetSentiment.where(:tracker_id => key.id, :date => params[:date])
      list.destroy_all
      render status: 200, json: {
        message: "Successfully delted Tweet Sentiment"
      }.to_json
    else
      render status: 422, json: {
        message: "Failed to delete Tweet Sentiment"
      }.to_json
    end
  end

  private
    def json_params
      params.require(:tweet_sentiment).permit(:keyword, :date, :sentiment)
    end

    def admin_access
      head :unauthorized unless Rails.application.secrets.api_key == params[:api_key]
    end

end
