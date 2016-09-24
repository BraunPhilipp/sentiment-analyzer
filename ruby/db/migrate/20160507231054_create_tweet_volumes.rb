class CreateTweetVolumes < ActiveRecord::Migration
  def change
    create_table :tweet_volumes do |t|
      t.references :tracker, index: true, foreign_key: true
      t.datetime :date
      t.integer :volume

      t.timestamps null: false
    end
  end
end
