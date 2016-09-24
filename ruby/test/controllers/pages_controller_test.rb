require 'test_helper'

class PagesControllerTest < ActionController::TestCase
  test "should get home" do
    get :home
    assert_response :success
  end

  test "should get news" do
    get :news
    assert_response :success
  end

  test "should get tracker" do
    get :tracker
    assert_response :success
  end

  test "should get search" do
    get :search
    assert_response :success
  end

  test "should get contact" do
    get :contact
    assert_response :success
  end

  test "should get privacy" do
    get :privacy
    assert_response :success
  end

  test "should get legal" do
    get :legal
    assert_response :success
  end

end
