class Intention
  include Mongoid::Document
  include Mongoid::Timestamps

  PENDING_STATUS = 'pending'
  COMPLETE_STATUS = 'complete'

  field :data, type: Hash, default: {}
  field :status, type: String, default: PENDING_STATUS
  field :step, type: String, default: '1'

  belongs_to :user
  validates_inclusion_of :status, in: [PENDING_STATUS, COMPLETE_STATUS]

  def reset
    self.data = {}
  end

  def reset!
    reset
    save!
  end
end