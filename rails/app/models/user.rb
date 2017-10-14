class User
  include Mongoid::Document
  include Mongoid::Timestamps

  field :email, type: String
  field :full_name, type: String
  field :user_type, type: String
  field :session_id, type: String
  field :settings, type: Hash, default: {}
  field :data, type: Hash, default: {}
  field :registered, type: Boolean, default: false

  has_many :intentions, validate: false

  DESIGNER_TYPE = 'designer'
  CUSTOMER_TYPE = 'customer'
  UNDEFINED_TYPE = 'undefined'

  validates_inclusion_of :user_type, in: [DESIGNER_TYPE, CUSTOMER_TYPE, UNDEFINED_TYPE]
  validates_presence_of :email, :full_name, :session_id
  validates_uniqueness_of :email
end
