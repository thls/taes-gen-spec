class BackupManager
  # @param source_paths [Array] must be a non-empty array of valid file or directory paths
  # @param destination [String] must be a valid destination path for the backup
  # @param compression [String] must be one of: none, gzip, bzip2, xz
  # @param encryption [Boolean] must be a boolean indicating whether to encrypt the backup
  # @param retention_policy [Hash] must be a hash with backup retention policy settings
  # @return [Hash] a hash containing the backup location and metadata if backup was successful
  # @return [Hash] a hash with error information if backup creation failed
  # @raise [ArgumentError] the param source_paths is empty or contains invalid paths
  # @raise [ArgumentError] the param destination is empty or invalid
  # @raise [ArgumentError] the param compression is not one of the supported compression methods
  # @raise [IOError] insufficient disk space available for the backup
  def create_backup(source_paths, destination, compression, encryption, retention_policy)
    # TODO
  end

end