import { useCallback, useState } from 'react'
import { Upload, File, X } from 'lucide-react'
import { motion } from 'framer-motion'

interface FileUploadProps {
  onFileSelect: (file: File) => void
  accept?: string
  maxSize?: number
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  accept = '.pdf,.docx',
  maxSize = 10 * 1024 * 1024,
}) => {
  const [isDragging, setIsDragging] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleDragEnter = useCallback(() => {
    setIsDragging(true)
    setError(null)
  }, [])

  const handleDragLeave = useCallback(() => {
    setIsDragging(false)
  }, [])

  const handleFile = useCallback(
    (file: File) => {
      setError(null)

      if (file.size > maxSize) {
        setError(`File size exceeds ${maxSize / (1024 * 1024)}MB limit`)
        return
      }

      const validTypes = accept.split(',').map(t => t.trim())
      const fileType = `.${file.name.split('.').pop()}`
      if (!validTypes.includes(fileType)) {
        setError(`Invalid file type. Accepted: ${accept}`)
        return
      }

      setSelectedFile(file)
      onFileSelect(file)
    },
    [accept, maxSize, onFileSelect],
  )

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setIsDragging(false)

      const files = e.dataTransfer.files
      if (files.length > 0) {
        handleFile(files[0])
      }
    },
    [handleFile],
  )

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.currentTarget.files
    if (files && files.length > 0) {
      handleFile(files[0])
    }
  }

  const clearSelection = () => {
    setSelectedFile(null)
    setError(null)
  }

  return (
    <div className="w-full">
      <motion.div
        className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          isDragging
            ? 'border-accent bg-accent/10'
            : 'border-muted hover:border-accent/50'
        }`}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        whileHover={{ scale: 1.01 }}
      >
        <input
          type="file"
          accept={accept}
          onChange={handleChange}
          className="hidden"
          id="file-upload"
        />

        {!selectedFile ? (
          <label htmlFor="file-upload" className="cursor-pointer">
            <div className="flex flex-col items-center space-y-4">
              <motion.div
                animate={{ y: [0, -5, 0] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                <Upload className="w-12 h-12 text-accent mx-auto" />
              </motion.div>
              <div>
                <p className="text-foreground font-semibold">
                  Drag and drop your resume
                </p>
                <p className="text-muted-foreground text-sm">
                  or click to browse (PDF or DOCX, max {maxSize / (1024 * 1024)}MB)
                </p>
              </div>
            </div>
          </label>
        ) : (
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <File className="w-8 h-8 text-accent" />
              <div className="text-left">
                <p className="text-foreground font-semibold">{selectedFile.name}</p>
                <p className="text-muted-foreground text-sm">
                  {(selectedFile.size / 1024).toFixed(2)} KB
                </p>
              </div>
            </div>
            <button
              onClick={clearSelection}
              className="p-2 hover:bg-muted rounded-lg transition"
            >
              <X size={20} />
            </button>
          </div>
        )}
      </motion.div>

      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-3 p-3 bg-destructive/10 border border-destructive/50 rounded-lg text-destructive text-sm"
        >
          {error}
        </motion.div>
      )}
    </div>
  )
}

export default FileUpload
