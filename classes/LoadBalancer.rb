class LoadBalancer
  # @param request [Hash] must be a hash with request information including method and path
  # @param backend_pool [Array] must be a non-empty array of backend server addresses
  # @param algorithm [String] must be one of: round_robin, least_connections, ip_hash, weighted
  # @param health_check [Boolean] must be a boolean indicating whether to perform health checks
  # @param sticky_session [Boolean] must be a boolean indicating whether to use sticky sessions
  # @return [Hash] a hash containing the selected backend server and routing information if routing was successful
  # @return [Hash] a hash indicating no healthy backends available if all servers are down
  # @raise [ArgumentError] the param request is missing required method or path keys
  # @raise [ArgumentError] the param backend_pool is empty or not an array
  # @raise [ArgumentError] the param algorithm is not one of the supported load balancing algorithms
  # @raise [RuntimeError] all backend servers in the pool are unhealthy or unavailable
  def route_request(request, backend_pool, algorithm, health_check, sticky_session)
    # TODO
  end

end