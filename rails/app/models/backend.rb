require "net/http"
require "uri"
require "json"

class Backend
  RANDOM_IMAGES = "http://flask:5000/"
  IMAGES_URL = "brandimages/"

  def self.get_rand_images
    results = { "data" => [] }

    uri = URI.parse(RANDOM_IMAGES + "random-samples")
    response = Net::HTTP.get_response(uri)

    if response.code != "200"
      puts uri
      puts response.body 
    end

    if response.code == "200"
      results = JSON.parse(response.body)
    end


    results["data"]
  end

  def self.similar(id:, radius: 150, n: 10, init_radius: 200)
    results = { "data" => [] }

    uri = URI.parse(RANDOM_IMAGES + "images/#{id}?radius=#{radius}&n=#{n}&initial-radius=#{init_radius}")
    response = Net::HTTP.get_response(uri)

    if response.code != "200"
      puts uri
      puts response.body 
    end

    if response.code == "200"
      results = JSON.parse(response.body)
    end


    results["data"]
  end
end