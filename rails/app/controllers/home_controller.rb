class HomeController < ApplicationController
  before_action do
    @user_holder = Interaction.new_place_holder_user(session_id: session.id)
    @intention = Interaction.current_intention(user: @user_holder)
  end

  def index
    @intention.reset!
    @intention.save!
  end

  def brief ; end
  def hello ; end

  def search
    if params[:boton] == "searched"
      @intention.reset!
      @intention.data["category"] = params[:category]
      @intention.data["industry"] = params[:industry]
      @intention.save!      
      redirect_to :zoom
    end    
  end

  def zoom
    @images = []

    if params[:img_id].blank? && @intention.data["counter"].blank?
      @intention.data["counter"] = Interaction::ZOOM_STEPS
      @intention.data["radius"] = 200

      @images = Backend.get_rand_images.each_slice(4)

      @intention.data["last_image"] = @images.first.try(:first).try(:[], "filename")
      @intention.data["rand_img"] = @images.to_a.flatten.map{|o| o.try(:[], "filename")}.sample(3)[0]
    end

    if params[:img_id].present? && @intention.data["counter"] >= 1
      @intention.data["last_image"] = params[:last_image]
      @intention.data["last_image_prob"] = params[:last_image_prob]
      @intention.data["last_image_id"] = params[:img_id]

      @images = Backend.similar(id: params[:img_id],
                                radius: @intention.data["radius"],
                                n: 10,
                                init_radius: 200).each_slice(4)

      @intention.data["counter"] -= 1
      @intention.data["radius"] -= 27
    end

    @intention.save!

    if @intention.data["counter"] == 0
      redirect_to :summary
    end
  end

  def summary
    @image = Backend.similar(id: @intention.data["last_image_id"],
                          radius: @intention.data["radius"],
                          n: 10,
                          init_radius: 200).sample
  end

  def designers
    data_ = Backend.similar_designers(id: @intention.data["last_image_id"],
                          radius: @intention.data["radius"],
                          n: 10,
                          init_radius: 200)

    @designers = Interaction.map_designers(data_)
  end
end
