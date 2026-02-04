import React, { useState } from 'react';
import axios from 'axios';
import { Upload, Shirt, Sparkles, Loader2, ArrowRight, Image as ImageIcon } from 'lucide-react';
import { useDropzone } from 'react-dropzone';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { motion, AnimatePresence } from 'framer-motion';

function cn(...inputs) {
  return twMerge(clsx(inputs));
}

function App() {
  const [itemUrl, setItemUrl] = useState('');
  const [itemImages, setItemImages] = useState([]);
  const [selectedItemImage, setSelectedItemImage] = useState(null);
  const [itemImageBase64, setItemImageBase64] = useState(null); // New state for good_img
  const [personImage, setPersonImage] = useState(null);
  const [personImageUrl, setPersonImageUrl] = useState(null);
  const [personImageBase64, setPersonImageBase64] = useState(null);
  const [previewPersonUrl, setPreviewPersonUrl] = useState(null);
  const [resultImages, setResultImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState('');
  const [error, setError] = useState('');

  // Item Image Upload Handler
//   const onItemDrop = async (acceptedFiles) => {
//     const file = acceptedFiles[0];
//     if (file) {
//       // Create a local URL for preview
//       const previewUrl = URL.createObjectURL(file);
//       setItemImages([previewUrl]);
      
//       // Convert to Base64
//       const reader = new FileReader();
//       reader.onload = () => {
//         setItemImageBase64(reader.result);
//       };
//       reader.readAsDataURL(file);
//     }
//   };

//   const { 
//     getRootProps: getItemRootProps, 
//     getInputProps: getItemInputProps, 
//     isDragActive: isItemDragActive 
//   } = useDropzone({
//     onDrop: onItemDrop,
//     accept: { 'image/*': [] },
//     multiple: false
//   });

  // Person Image Upload Handler
  const onPersonDrop = async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setPersonImage(file);
      setPreviewPersonUrl(URL.createObjectURL(file));
      
      // Convert to Base64
      const reader = new FileReader();
      reader.onload = () => {
        setPersonImageBase64(reader.result);
      };
      reader.readAsDataURL(file);

      // 移除上传逻辑，仅本地处理
      // await uploadPersonImage(file);
    }
  };

  const { 
    getRootProps: getPersonRootProps, 
    getInputProps: getPersonInputProps, 
    isDragActive: isPersonDragActive 
  } = useDropzone({
    onDrop: onPersonDrop,
    accept: { 'image/*': [] },
    multiple: false
  });

  // const uploadPersonImage = async (file) => {
  //   setLoading(true);
  //   setLoadingStep('正在上传图片...');
  //   setError('');
  //   const formData = new FormData();
  //   formData.append('file', file);
  //
  //   try {
  //     const res = await axios.post('/api/upload_file', formData, {
  //       headers: { 'Content-Type': 'multipart/form-data' }
  //     });
  //     if (res.data.code === 200 && res.data.data) {
  //       setPersonImageUrl(res.data.data.url || res.data.data.path);
  //     } else {
  //       setError(res.data.msg || '上传失败');
  //     }
  //   } catch (err) {
  //     setError('上传图片时发生错误');
  //     console.error(err);
  //   } finally {
  //     setLoading(false);
  //     setLoadingStep('');
  //   }
  // };

  const fetchItemData = async () => {
    if (!itemUrl) return;
    setLoading(true);
    setLoadingStep('正在解析商品信息...');
    setError('');
    try {
      // 假设这是 GET 或者 POST 请求，根据之前代码是 POST
      const res = await axios.post('/api/get_item_data', null, {
        params: { text: itemUrl }
      });
      if (res.data.code === 200) {
        // 从返回的数据中提取商品图片
        let imgs = [];
        let item_imgs=res.data.data.item_imgs || []
        let prop_imgs=res.data.data.prop_imgs || []
        // 去重
        imgs=[...item_imgs,...prop_imgs]
        imgs = [...new Set(imgs)];

        setItemImages(imgs);
        if (imgs.length > 0) {
            setSelectedItemImage(imgs[0]);
        } else {
            setError('未找到商品图片');
        }
      } else {
        setError(res.data.msg || '解析商品失败');
      }
    } catch (err) {
      setError('解析商品时发生错误');
      console.error(err);
    } finally {
      setLoading(false);
      setLoadingStep('');
    }
  };

  const [previewImage, setPreviewImage] = useState(null); // State for full screen preview

  const handleTryOn = async () => {
    if (!personImageBase64) {
      setError('请先上传您的照片');
      return;
    }
    if (!selectedItemImage) {
      setError('请选择一张商品图片');
      return;
    }

    setLoading(true);
    setLoadingStep('AI正在进行试用，可能需要几十秒，请耐心等待...');
    setError('');
    setResultImages([]);

    try {
      const payload = {
        person_img: personImageBase64, // Base64
        good_img: selectedItemImage     // URL
      };
      
      console.log('Try-on payload:', payload); // Debug log

      const res = await axios.post('/api/try_on', payload);
      
      if (res.data.code === 200) {
        setResultImages(res.data.data); // data 应该是 URL 列表
      } else {
        setError(res.data.msg || '试用失败');
      }
    } catch (err) {
      setError('试用请求发生错误');
      console.error(err);
    } finally {
      setLoading(false);
      setLoadingStep('');
    }
  };

  return (
    <div className="min-h-screen text-white p-8 font-sans">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="mb-12 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-purple-600 p-2 rounded-xl">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-400">
              自动商品试用
            </h1>
          </div>
        </header>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          
          {/* Left Column: Item Input */}
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-6"
          >
            <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Shirt className="w-5 h-5 text-purple-400" />
                第一步：输入商品
              </h2>
              <div className="flex flex-col gap-3 mb-4">
                <textarea
                  value={itemUrl}
                  onChange={(e) => setItemUrl(e.target.value)}
                  placeholder="粘贴淘宝/天猫/京东商品链接，支持直接粘贴完整分享口令"
                  className="w-full h-32 bg-slate-900 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all resize-none"
                />
                <button
                  onClick={fetchItemData}
                  disabled={loading || !itemUrl}
                  className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-slate-700 disabled:cursor-not-allowed px-6 py-3 rounded-lg font-medium transition-colors"
                >
                  解析商品
                </button>
              </div>

              {/* Item Preview */}
              <div className="bg-slate-900/50 rounded-xl border border-slate-700/50 p-4 min-h-[16rem]">
                {itemImages.length > 0 ? (
                  <div className="space-y-4">
                    <div className="h-64 rounded-lg overflow-hidden bg-slate-800 flex items-center justify-center">
                        <img 
                            src={selectedItemImage} 
                            alt="Selected Item" 
                            className="w-full h-full object-contain" 
                        />
                    </div>
                    <div className="grid grid-cols-4 gap-2 overflow-y-auto max-h-32 pr-2">
                        {itemImages.map((img, idx) => (
                            <button
                                key={idx}
                                onClick={() => setSelectedItemImage(img)}
                                className={cn(
                                    "relative aspect-square rounded-lg overflow-hidden border-2 transition-all",
                                    selectedItemImage === img 
                                        ? "border-purple-500 ring-2 ring-purple-500/30" 
                                        : "border-transparent hover:border-slate-600"
                                )}
                            >
                                <img 
                                    src={img} 
                                    alt={`Option ${idx + 1}`} 
                                    className="w-full h-full object-cover" 
                                />
                            </button>
                        ))}
                    </div>
                  </div>
                ) : (
                  <div className="h-full flex flex-col items-center justify-center text-slate-500 gap-2">
                    <Shirt className="w-8 h-8 opacity-50" />
                    <span className="text-sm">商品图片将显示在这里</span>
                  </div>
                )}
              </div>
            </div>
          </motion.div>

          {/* Right Column: Person Upload */}
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-6"
          >
            <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Upload className="w-5 h-5 text-pink-400" />
                第二步：上传照片
              </h2>
              
              <div 
                {...getPersonRootProps()} 
                className={cn(
                  "h-80 border-2 border-dashed rounded-xl flex flex-col items-center justify-center cursor-pointer transition-all duration-300 relative overflow-hidden",
                  isPersonDragActive ? "border-pink-500 bg-pink-500/10" : "border-slate-600 hover:border-pink-400 hover:bg-slate-800/80",
                  previewPersonUrl ? "border-solid border-pink-500/50" : ""
                )}
              >
                <input {...getPersonInputProps()} />
                {previewPersonUrl ? (
                  <>
                    <img src={previewPersonUrl} alt="Person" className="w-full h-full object-contain z-10" />
                    <div className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity z-20">
                      <p className="text-white font-medium">点击更换照片</p>
                    </div>
                  </>
                ) : (
                  <div className="text-center p-6">
                    <div className="w-16 h-16 bg-slate-700 rounded-full flex items-center justify-center mx-auto mb-4">
                      <ImageIcon className="w-8 h-8 text-slate-400" />
                    </div>
                    <p className="text-lg font-medium mb-1">点击或拖拽上传</p>
                    <p className="text-sm text-slate-400">支持 JPG, PNG 格式</p>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        </div>

        {/* Action Button */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-12 flex flex-col items-center"
        >
          {error && (
            <div className="mb-4 text-red-400 bg-red-400/10 px-4 py-2 rounded-lg border border-red-400/20">
              {error}
            </div>
          )}
          
          <button
            onClick={handleTryOn}
            disabled={loading || !personImageBase64 || !selectedItemImage}
            className="group relative px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full text-xl font-bold shadow-lg shadow-purple-500/25 hover:shadow-purple-500/40 disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none transition-all overflow-hidden"
          >
            <div className="relative z-10 flex items-center gap-2">
              {loading ? (
                <>
                  <Loader2 className="w-6 h-6 animate-spin" />
                  <span>{loadingStep}</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-6 h-6" />
                  <span>立即生成试用效果</span>
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </div>
            {!loading && (
              <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
            )}
          </button>
        </motion.div>

        {/* Results Section */}
        <AnimatePresence>
          {resultImages.length > 0 && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-16 overflow-hidden"
            >
              <h2 className="text-3xl font-bold text-center mb-8 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-400">
                试用结果
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
                {resultImages.map((img, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.1 }}
                    className="bg-slate-800 rounded-2xl overflow-hidden border border-slate-700 shadow-2xl"
                  >
                    <img 
                        src={img} 
                        alt={`Result ${index + 1}`} 
                        className="w-full h-auto cursor-pointer hover:opacity-90 transition-opacity" 
                        onClick={() => setPreviewImage(img)}
                    />
                    <div className="p-4 flex justify-between items-center bg-slate-900/50">
                      <span className="text-slate-400">生成结果 #{index + 1}</span>
                      <button 
                        onClick={() => setPreviewImage(img)}
                        className="text-purple-400 hover:text-purple-300 text-sm font-medium"
                      >
                        查看大图
                      </button>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Full Screen Image Preview Modal */}
        <AnimatePresence>
            {previewImage && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    onClick={() => setPreviewImage(null)}
                    className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 p-4 backdrop-blur-sm"
                >
                    <motion.img
                        initial={{ scale: 0.9 }}
                        animate={{ scale: 1 }}
                        exit={{ scale: 0.9 }}
                        src={previewImage}
                        alt="Full Screen Preview"
                        className="max-w-full max-h-full object-contain rounded-lg shadow-2xl"
                        onClick={(e) => e.stopPropagation()} 
                    />
                    <button
                        onClick={() => setPreviewImage(null)}
                        className="absolute top-4 right-4 text-white/70 hover:text-white bg-white/10 hover:bg-white/20 rounded-full p-2 transition-colors"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                    </button>
                </motion.div>
            )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default App;
