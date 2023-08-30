module.exports = {
  presets: [
    // ts预制
    [
      '@babel/preset-typescript',
      {
        allExtensions: true, // 支持所有文件扩展名，否则在vue文件中使用ts会报错
      },
    ],
    //将基础的ES6语法向下转译，兼容不同的浏览器
    [
      '@babel/preset-env',
      {
        useBuiltIns: 'usage',
        corejs: '3',
      },
    ],
  ],
};
