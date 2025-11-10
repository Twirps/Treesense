import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Upload, CheckCircle2, AlertCircle, Info } from "lucide-react";

// Mock tree data (in production, this would come from the ML model)
const mockTreeData = [
  {
    name: "Red Maple",
    scientificName: "Acer rubrum",
    confidence: 92,
    description: "A medium to large deciduous tree native to eastern North America. Known for its vibrant red fall foliage and adaptability to various soil conditions.",
    commonFeatures: [
      "Opposite leaf arrangement",
      "3-5 lobed leaves with serrated edges",
      "Red flowers in early spring",
      "Gray bark with shallow ridges"
    ]
  },
  {
    name: "White Oak",
    scientificName: "Quercus alba",
    confidence: 85,
    description: "A large, long-lived deciduous tree native to eastern and central North America. Prized for its strength and beautiful wood.",
    commonFeatures: [
      "Rounded lobes on leaves",
      "Light gray scaly bark",
      "Acorns with warty cap",
      "Dense, spreading crown"
    ]
  },
  {
    name: "Loblolly Pine",
    scientificName: "Pinus taeda",
    confidence: 78,
    description: "A common pine tree in the southeastern United States. Fast-growing evergreen widely used in forestry.",
    commonFeatures: [
      "Long needles in bundles of 3",
      "Reddish-brown bark plates",
      "Large woody cones",
      "Tall straight trunk"
    ]
  }
];

const Results = () => {
  const navigate = useNavigate();
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [selectedTree] = useState(mockTreeData[0]); // In production, this would be the ML prediction

  useEffect(() => {
    const storedImage = sessionStorage.getItem("uploadedImage");
    if (!storedImage) {
      navigate("/");
      return;
    }
    setImageUrl(storedImage);
  }, [navigate]);

  const handleNewUpload = () => {
    sessionStorage.removeItem("uploadedImage");
    navigate("/");
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 85) return "text-[hsl(var(--success-green))]";
    if (confidence >= 70) return "text-[hsl(var(--warning-amber))]";
    return "text-muted-foreground";
  };

  const getConfidenceIcon = (confidence: number) => {
    if (confidence >= 85) return CheckCircle2;
    if (confidence >= 70) return AlertCircle;
    return Info;
  };

  if (!imageUrl) {
    return null;
  }

  const ConfidenceIcon = getConfidenceIcon(selectedTree.confidence);

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-secondary/20">
      {/* Header */}
      <div className="bg-card border-b border-border shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-6 flex items-center justify-between">
          <Button
            variant="ghost"
            onClick={() => navigate("/")}
            className="gap-2"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Button>
          <h1 className="text-2xl font-bold text-foreground">TreeSense Results</h1>
          <Button
            variant="hero"
            onClick={handleNewUpload}
            className="gap-2"
          >
            <Upload className="w-4 h-4" />
            New Upload
          </Button>
        </div>
      </div>

      {/* Results Content */}
      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Uploaded Image */}
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-foreground">Your Image</h2>
            <div className="rounded-2xl overflow-hidden shadow-lg border-2 border-border">
              <img
                src={imageUrl}
                alt="Uploaded tree"
                className="w-full h-auto object-cover"
              />
            </div>
          </div>

          {/* Identification Results */}
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold text-foreground mb-4">
                Identification Result
              </h2>
              
              {/* Main Result Card */}
              <div className="rounded-2xl bg-card border-2 border-primary shadow-lg p-8">
                <div className="flex items-start justify-between mb-6">
                  <div>
                    <h3 className="text-3xl font-bold text-foreground mb-2">
                      {selectedTree.name}
                    </h3>
                    <p className="text-lg italic text-muted-foreground">
                      {selectedTree.scientificName}
                    </p>
                  </div>
                  <div className="flex flex-col items-end gap-1">
                    <ConfidenceIcon className={`w-8 h-8 ${getConfidenceColor(selectedTree.confidence)}`} />
                    <span className={`text-3xl font-bold ${getConfidenceColor(selectedTree.confidence)}`}>
                      {selectedTree.confidence}%
                    </span>
                    <span className="text-xs text-muted-foreground">Confidence</span>
                  </div>
                </div>

                <div className="space-y-4">
                  <div>
                    <h4 className="font-semibold text-foreground mb-2">Description</h4>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {selectedTree.description}
                    </p>
                  </div>

                  <div>
                    <h4 className="font-semibold text-foreground mb-3">Common Features</h4>
                    <ul className="space-y-2">
                      {selectedTree.commonFeatures.map((feature, index) => (
                        <li key={index} className="flex items-start gap-2 text-sm text-muted-foreground">
                          <CheckCircle2 className="w-4 h-4 text-primary flex-shrink-0 mt-0.5" />
                          <span>{feature}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            {/* Alternative Matches */}
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-3">
                Other Possible Matches
              </h3>
              <div className="space-y-3">
                {mockTreeData.slice(1).map((tree, index) => (
                  <div
                    key={index}
                    className="rounded-xl bg-card border border-border p-4 hover:border-primary/50 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-semibold text-foreground">{tree.name}</h4>
                        <p className="text-sm italic text-muted-foreground">
                          {tree.scientificName}
                        </p>
                      </div>
                      <span className={`text-lg font-bold ${getConfidenceColor(tree.confidence)}`}>
                        {tree.confidence}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Results;
