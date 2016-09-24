class CreateTweetData < ActiveRecord::Migration
  def change
    create_table :tweet_data do |t|
      t.bigint :tweet_id
      t.datetime :tweet_date
      t.text :tweet_text
      t.string :tweet_lang
      t.integer :tweet_retweet_count
      t.integer :tweet_favorite_count
      t.bigint :tweet_user_id
      t.integer :tweet_user_verified
      t.integer :tweet_sentiment
      t.integer :tweet_score
      t.references :tracker, index: true, foreign_key: true

      t.timestamps null: false
    end
  end
end
