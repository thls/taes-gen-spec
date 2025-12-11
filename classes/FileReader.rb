class FileReader
  # @param path [String] cannot be empty
  # @return [String] the response body or content as a string
  # @raise [Errno::ENOENT] the file at the param path does not exist
  def read(path)
    # TODO
  end

  # @param path [String]
  # @return [Boolean] true if the condition is met
  # @return [Boolean] false if the condition is not met
  def exists?(path)
    # TODO
  end

end