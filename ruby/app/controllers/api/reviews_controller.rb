class Api::ReviewsController < Api::ApiController

  before_filter :admin_access
  # rails generate model tweet_sentiment tracker:references date:datetime sentiment:integer
  # bundle exec rake db:migrate

  def index
    render json: Review.all
  end

  # curl -i -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"text":"This is bad!", "category":"english", "score":"0"}' http://localhost:3000/api/reviews

  def create
    new_reviews = json_params

    new_reviews.each do |rev|
      list = Review.new(rev)
      if !list.save
        render status: 402, json: {
          message: "Could not create new Review!",
          review: list
        }.to_json and return
      end
    end

  else
    render status: 200, json: {
      message: "New reviews were created!"
    }.to_json

  end

  def search
    list = Review.where(:category => params[:q])
    if params.has_key?(:limit)
      list = list.limit(params[:limit])
    end
    render json: list
  end

  private
    def list_params
      params.require(:review).permit(:text, :category, :score)
    end

    def json_params
      params.permit(:data => [:text, :category, :score]).require(:data)
    end

    def admin_access
      head :unauthorized unless Rails.application.secrets.api_key == params[:api_key]
    end

end
