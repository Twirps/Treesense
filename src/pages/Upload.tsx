import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { UploadZone } from "@/components/UploadZone";
import { Leaf, Trees } from "lucide-react";
import { predictImage, loadModel } from "../lib/tfmodel";

const Upload = () => {
  const navigate = useNavigate();
  const [selectedImage, setSelectedImage] = useState<File | null>(null);

  const handleImageSelect = async (file: File) => {
    setSelectedImage(file);
  
    // Create an image element for prediction
    const img = new Image();
    img.src = URL.createObjectURL(file);
  
    img.onload = async () => {
      await loadModel(); // make sure model is loaded
      const prediction = await predictImage(img);
  
      // Store prediction in sessionStorage (or state)
      sessionStorage.setItem("prediction", JSON.stringify(prediction));
  
      // Navigate to results page
      navigate("/results");
    };
  };  

  return (
    <div className="min-h-screen">
      {/* Modern Hero Section */}
      <div className="relative h-[600px] overflow-hidden bg-gradient-to-br from-[hsl(145,60%,25%)] via-[hsl(145,55%,30%)] to-[hsl(145,50%,35%)]">
        {/* Multi-Layer Pattern Background */}
        <div className="absolute inset-0">
          {/* Dot Grid Pattern */}
          <div 
            className="absolute inset-0 opacity-20"
            style={{
              backgroundImage: 'radial-gradient(circle, hsl(145 70% 50% / 0.3) 1.5px, transparent 1.5px)',
              backgroundSize: '32px 32px'
            }}
          />
          
          {/* Larger Grid Pattern */}
          <div 
            className="absolute inset-0 opacity-10"
            style={{
              backgroundImage: 'linear-gradient(hsl(145 70% 50% / 0.15) 1px, transparent 1px), linear-gradient(90deg, hsl(145 70% 50% / 0.15) 1px, transparent 1px)',
              backgroundSize: '64px 64px'
            }}
          />
          
          {/* Diagonal Accent Lines */}
          <div 
            className="absolute inset-0 opacity-5"
            style={{
              backgroundImage: 'repeating-linear-gradient(45deg, transparent, transparent 40px, hsl(145 70% 50% / 0.3) 40px, hsl(145 70% 50% / 0.3) 80px)'
            }}
          />
          
          {/* Organic Blob Shapes */}
          <div className="absolute top-20 right-20 w-96 h-96 bg-accent/10 rounded-full blur-3xl" />
          <div className="absolute bottom-20 left-20 w-80 h-80 bg-primary/10 rounded-full blur-3xl" />
        </div>
        
        {/* Mesh Gradient Overlay */}
        <div className="absolute inset-0 bg-[radial-gradient(at_0%_0%,hsl(145,70%,40%,0.3)_0px,transparent_50%),radial-gradient(at_100%_100%,hsl(145,60%,50%,0.2)_0px,transparent_50%)]" />
        
        {/* Content Container */}
        <div className="relative h-full max-w-7xl mx-auto px-4 flex items-center">
          <div className="grid lg:grid-cols-2 gap-12 items-center w-full">
            {/* Left Content */}
            <div className="space-y-8">
              {/* Glassmorphic Badge */}
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-md border border-white/20 animate-fade-in-up">
                <Leaf className="w-4 h-4 text-[hsl(145,50%,85%)]" />
                <span className="text-sm text-white/90 font-mono tracking-wider">AI-Powered Tree Recognition</span>
              </div>
              
              {/* Main Heading */}
              <div className="space-y-4 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
                <div className="flex items-center gap-4">
                  <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-white/20 to-white/5 backdrop-blur-md border border-white/30 flex items-center justify-center shadow-2xl">
                    <Trees className="w-10 h-10 text-white" />
                  </div>
                  <h1 className="text-6xl md:text-7xl font-bold text-gradient tracking-normal antialiased pr-2" style={{ textShadow: '0 2px 40px rgba(255,255,255,0.1)' }}>
                    TreeSense
                  </h1>
                </div>
                <p className="text-2xl md:text-3xl text-white/80 font-thin leading-[1.2] tracking-wide">
                  Identify UNCC Campus Trees with Computer Vision
                </p>
              </div>
              
              {/* Feature Pills */}
              <div className="flex flex-wrap gap-3 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
                <div className="px-4 py-2 rounded-full bg-white/5 backdrop-blur-sm border border-white/10 text-white/80 text-base font-semibold tracking-wider">
                  🌳 15+ Tree Species
                </div>
                <div className="px-4 py-2 rounded-full bg-white/5 backdrop-blur-sm border border-white/10 text-white/80 text-base font-semibold tracking-wider">
                  📸 Instant Recognition
                </div>
                <div className="px-4 py-2 rounded-full bg-white/5 backdrop-blur-sm border border-white/10 text-white/80 text-base font-semibold tracking-wider">
                  🎓 Campus-Specific
                </div>
              </div>
            </div>
            
          </div>
        </div>
        
        {/* Scroll Indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
          <div className="w-6 h-10 border-2 border-white/30 rounded-full flex items-start justify-center p-2">
            <div className="w-1.5 h-1.5 bg-white/60 rounded-full" />
          </div>
        </div>
      </div>

      {/* Upload Section */}
      <div className="max-w-6xl mx-auto px-4 py-20">
        <div className="mb-16 text-center space-y-4">
          <h2 className="text-4xl md:text-5xl font-black text-foreground tracking-tight pb-2">
            Start Identifying Trees
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto font-light leading-relaxed">
            Upload a clear photo of the tree's leaves, bark, or overall structure. 
            Our AI model recognizes 10-15 common species found on campus.
          </p>
        </div>

        <UploadZone onImageSelect={handleImageSelect} />

      </div>
    </div>
  );
};

export default Upload;
