class HomeController < ApplicationController
  before_action do
    session[:zoom] = (session.try(:[], :zoom) || {}).with_indifferent_access
  end

  def index
    session[:zoom] = {}
  end
  def brief ; end
  def hello ; end

  def search
    session[:zoom] = {}
    if params[:boton] == "searched"
      data = session[:data] || {}
      data[:category] = params[:category]
      data[:industry] = params[:industry]
      session[:data] = data
      redirect_to :tags
    end

    
  end

  def tags
    session[:zoom] = {}
    if params[:boton] == "tags"
      data = session[:data] || {}
      #TODO store tags
      redirect_to :zoom
    end
  end

  def zoom
    zoom = session[:zoom] || {}
    @images = []
    

    if params[:img_id].blank? && zoom[:counter].blank?
      zoom[:counter] = 5
      zoom[:radius] = 200
      @images = Backend.get_rand_images.each_slice(4)
      zoom[:last_image] = @images.first.try(:first).try(:[], "filename")
      zoom[:rand_img] = @images.to_a.flatten.map{|o| o.try(:[], "filename")}.sample(3)[0]

      session[:zoom] = zoom
    end

    if params[:img_id].present? && zoom[:counter] >= 1
      zoom[:last_image] = params[:last_image]
      zoom[:last_image_prob] = params[:last_image_prob]

      @images = Backend.similar(id: params[:img_id],
                                radius: zoom[:radius],
                                n: 10,
                                init_radius: 200).each_slice(4)
      zoom[:counter] -= 1
      zoom[:radius] -= 27
      session[:zoom] = zoom
    end

    if zoom[:counter] == 0
      data = session[:data] || {}
      #TODO store image
      redirect_to :summary
    end
  end

  def summary
  end
end
