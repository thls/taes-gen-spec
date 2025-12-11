class DataTransformer
  # @param source_format [String] must be one of: json, xml, csv, yaml
  # @param target_format [String] must be one of: json, xml, csv, yaml
  # @param data [Object] must not be nil and must be parseable in the source format
  # @param options [Hash] must be a hash with valid transformation options
  # @return [String] the transformed data as a string in the target format
  # @return [String] an empty string if the transformation resulted in no data
  # @raise [ArgumentError] the param source_format is not a supported format
  # @raise [ArgumentError] the param target_format is not a supported format
  # @raise [ArgumentError] the param data is nil or cannot be parsed
  # @raise [RuntimeError] the transformation failed due to incompatible data structure
  def transform_dataset(source_format, target_format, data, options)
    # TODO
  end

end