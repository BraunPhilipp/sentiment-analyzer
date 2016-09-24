# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20160507231121) do

  create_table "reviews", force: :cascade do |t|
    t.text     "text",       limit: 65535
    t.string   "category",   limit: 255
    t.integer  "score",      limit: 4
    t.datetime "created_at",               null: false
    t.datetime "updated_at",               null: false
  end

  create_table "trackers", force: :cascade do |t|
    t.string   "keyword",    limit: 255
    t.integer  "volume",     limit: 4
    t.integer  "min_id",     limit: 8
    t.integer  "max_id",     limit: 8
    t.datetime "created_at",             null: false
    t.datetime "updated_at",             null: false
  end

  create_table "tweet_data", force: :cascade do |t|
    t.integer  "tweet_id",             limit: 8
    t.datetime "tweet_date"
    t.text     "tweet_text",           limit: 65535
    t.string   "tweet_lang",           limit: 255
    t.integer  "tweet_retweet_count",  limit: 4
    t.integer  "tweet_favorite_count", limit: 4
    t.integer  "tweet_user_id",        limit: 8
    t.integer  "tweet_user_verified",  limit: 4
    t.integer  "tweet_sentiment",      limit: 4
    t.integer  "tweet_score",          limit: 4
    t.integer  "tracker_id",           limit: 4
    t.datetime "created_at",                         null: false
    t.datetime "updated_at",                         null: false
  end

  add_index "tweet_data", ["tracker_id"], name: "index_tweet_data_on_tracker_id", using: :btree

  create_table "tweet_sentiments", force: :cascade do |t|
    t.integer  "tracker_id", limit: 4
    t.datetime "date"
    t.integer  "sentiment",  limit: 4
    t.datetime "created_at",           null: false
    t.datetime "updated_at",           null: false
  end

  add_index "tweet_sentiments", ["tracker_id"], name: "index_tweet_sentiments_on_tracker_id", using: :btree

  create_table "tweet_volumes", force: :cascade do |t|
    t.integer  "tracker_id", limit: 4
    t.datetime "date"
    t.integer  "volume",     limit: 4
    t.datetime "created_at",           null: false
    t.datetime "updated_at",           null: false
  end

  add_index "tweet_volumes", ["tracker_id"], name: "index_tweet_volumes_on_tracker_id", using: :btree

  add_foreign_key "tweet_data", "trackers"
  add_foreign_key "tweet_sentiments", "trackers"
  add_foreign_key "tweet_volumes", "trackers"
end
