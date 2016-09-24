class CreateTweetSentiments < ActiveRecord::Migration
  def change
    create_table :tweet_sentiments do |t|
      t.references :tracker, index: true, foreign_key: true
      t.datetime :date
      t.integer :sentiment

      t.timestamps null: false
    end
  end
end
