import * as tf from '@tensorflow/tfjs';

let model: tf.LayersModel | null = null;
let classMapping: Record<number, string> | null = null;

export async function loadModel() {
  if (!model) {
    model = await tf.loadLayersModel('/model_tfjs/model.json');
    const response = await fetch('/model_tfjs/class_mapping.json');
    classMapping = await response.json();
    console.log('Model and class mapping loaded!');
  }
  return model;
}

export async function predictImage(imageElement: HTMLImageElement) {
  if (!model) await loadModel();

  const tensor = tf.browser.fromPixels(imageElement)
    .resizeNearestNeighbor([224, 224])
    .toFloat()
    .div(tf.scalar(255.0))
    .expandDims();

  const predictions = model.predict(tensor) as tf.Tensor;
  const probs = (await predictions.array()) as number[][];
  const maxIndex = probs[0].indexOf(Math.max(...probs[0]));
  const className = classMapping![maxIndex];

  return { className, confidence: probs[0][maxIndex] };
}
