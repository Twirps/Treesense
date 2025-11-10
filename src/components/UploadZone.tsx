import { useState, useCallback } from "react";
import { Upload, Camera } from "lucide-react";
import { Button } from "@/components/ui/button";

interface UploadZoneProps {
  onImageSelect: (file: File) => void;
}

export const UploadZone = ({ onImageSelect }: UploadZoneProps) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);
      
      const files = Array.from(e.dataTransfer.files);
      const imageFile = files.find((file) => file.type.startsWith("image/"));
      
      if (imageFile) {
        onImageSelect(imageFile);
      }
    },
    [onImageSelect]
  );

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) {
        onImageSelect(file);
      }
    },
    [onImageSelect]
  );

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`
        relative rounded-3xl p-16 text-center
        bg-white/40 backdrop-blur-xl border-2
        transition-all duration-500 ease-out
        ${
          isDragging
            ? "border-primary bg-primary/10 scale-[1.01] shadow-[0_0_60px_hsl(145,70%,50%,0.4)]"
            : "border-primary/30 hover:border-primary/50 hover:bg-white/50 hover:scale-[1.005] shadow-xl hover:shadow-2xl"
        }
      `}
    >
      {/* Gradient Border Effect */}
      <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-primary/20 via-accent/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
      
      <div className="relative flex flex-col items-center gap-8">
        {/* Animated Icon with Ring */}
        <div className="relative">
          <div className={`absolute inset-0 rounded-full bg-gradient-to-br from-primary to-accent blur-xl opacity-50 ${isDragging ? 'animate-pulse' : ''}`} />
          <div className={`relative w-24 h-24 rounded-full bg-gradient-to-br from-primary via-accent to-primary flex items-center justify-center shadow-2xl transition-transform duration-300 ${isDragging ? 'scale-110 rotate-12' : 'hover:scale-105'}`}>
            <Upload className="w-12 h-12 text-white" />
          </div>
          {/* Rotating Ring */}
          <div className={`absolute -inset-2 rounded-full border-2 border-dashed border-primary/40 ${isDragging ? 'animate-spin' : ''}`} style={{ animationDuration: '3s' }} />
        </div>
        
        <div className="space-y-3">
          <h3 className="text-2xl font-bold text-foreground tracking-tight">
            {isDragging ? "Drop your image here" : "Upload a tree image"}
          </h3>
          <p className="text-base text-muted-foreground max-w-md mx-auto leading-relaxed">
            Take a photo of a tree's leaves, bark, or overall shape to identify the species
          </p>
        </div>

        <div className="flex gap-4 flex-wrap justify-center">
          <Button
            variant="default"
            size="lg"
            onClick={() => document.getElementById("file-input")?.click()}
            className="bg-gradient-to-br from-primary to-accent hover:from-primary/90 hover:to-accent/90 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
          >
            <Upload className="w-5 h-5" />
            Choose File
          </Button>
          
          <Button
            variant="outline"
            size="lg"
            onClick={() => document.getElementById("camera-input")?.click()}
            className="border-2 border-primary bg-white/60 backdrop-blur-sm hover:bg-primary hover:text-white shadow-md hover:shadow-lg transition-all duration-300"
          >
            <Camera className="w-5 h-5" />
            Take Photo
          </Button>
        </div>

        <input
          id="file-input"
          type="file"
          accept="image/*"
          onChange={handleFileInput}
          className="hidden"
        />
        
        <input
          id="camera-input"
          type="file"
          accept="image/*"
          capture="environment"
          onChange={handleFileInput}
          className="hidden"
        />
      </div>
    </div>
  );
};
