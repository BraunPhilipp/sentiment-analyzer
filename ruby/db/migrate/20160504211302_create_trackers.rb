class CreateTrackers < ActiveRecord::Migration
  def change
    create_table :trackers do |t|
      t.string :keyword
      t.integer :volume
      t.bigint :min_id
      t.bigint :max_id

      t.timestamps null: false
    end
  end
end
