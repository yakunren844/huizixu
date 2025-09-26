import os

import pandas as pd


def extract_merge_and_split_advanced(excel_file_path, output_dir, chunk_size=10000, 
                                   required_columns=None, include_source=True,
                                   file_prefix="part", timestamp=False):
    """
    读取Excel文件中的所有Sheet，提取指定列，合并数据，并按数量限制分割保存（增强版本）
    
    Args:
        excel_file_path: Excel文件路径
        output_dir: 输出目录
        chunk_size: 每个分割文件的最大行数
        required_columns: 需要保留的列列表，默认为['监测名单', '证件号码', '类型']
        include_source: 是否包含来源Sheet信息
        file_prefix: 文件前缀
        timestamp: 是否在文件名中添加时间戳
    
    Returns:
        list: 保存的文件路径列表
    """
    # 设置默认所需列
    if required_columns is None:
        required_columns = ['监测名单', '证件号码', '类型']
    
    # 检查文件是否存在
    if not os.path.exists(excel_file_path):
        raise FileNotFoundError(f"文件不存在: {excel_file_path}")
    
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取Excel文件中的所有Sheet
    try:
        all_sheets = pd.read_excel(excel_file_path, sheet_name=None)
    except Exception as e:
        raise Exception(f"读取Excel文件失败: {str(e)}")
    
    # 处理每个Sheet，提取所需列
    processed_sheets = []
    sheet_names = []
    
    for sheet_name, df in all_sheets.items():
        # 检查是否存在所需的列
        available_columns = [col for col in required_columns if col in df.columns]
        
        if not available_columns:
            print(f"警告: Sheet '{sheet_name}' 中没有找到任何所需列，跳过该Sheet")
            continue
        
        # 提取所需的列
        extracted_df = df[available_columns].copy()
        
        # 添加缺失的列并填充NaN
        for col in required_columns:
            if col not in extracted_df.columns:
                extracted_df[col] = None
        
        # 重新排列列顺序
        extracted_df = extracted_df[required_columns]
        
        # 添加Sheet名称作为来源标识（如果启用）
        if include_source:
            extracted_df['来源Sheet'] = sheet_name
        
        processed_sheets.append(extracted_df)
        sheet_names.append(sheet_name)
    
    # 检查是否有可合并的数据
    if not processed_sheets:
        raise ValueError("所有Sheet中都没有找到所需的列，无法合并")
    
    # 合并所有处理后的Sheet
    merged_df = pd.concat(processed_sheets, ignore_index=True)
    
    print(f"成功处理了 {len(processed_sheets)} 个Sheet: {sheet_names}")
    print(f"合并后的数据形状: {merged_df.shape}")
    
    # 计算需要分割的文件数量
    total_rows = len(merged_df)
    num_files = math.ceil(total_rows / chunk_size)
    
    print(f"总行数: {total_rows}, 每个文件最多 {chunk_size} 行, 需要分割为 {num_files} 个文件")
    
    # 生成时间戳（如果启用）
    ts = ""
    if timestamp:
        ts = f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # 分割并保存文件
    saved_files = []
    
    for i in range(num_files):
        # 计算当前块的起始和结束索引
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, total_rows)
        
        # 提取当前块的数据
        chunk_df = merged_df.iloc[start_idx:end_idx]
        
        # 生成文件名
        file_name = f"{file_prefix}_{i+1:04d}{ts}.xlsx"
        file_path = os.path.join(output_dir, file_name)
        
        # 保存文件
        chunk_df.to_excel(file_path, index=False)
        saved_files.append(file_path)
        
        print(f"已保存: {file_name} (行 {start_idx+1}-{end_idx})")
    
    return saved_files

def create_summary_report(output_dir, saved_files, original_file):
    """
    创建分割操作的摘要报告
    
    Args:
        output_dir: 输出目录
        saved_files: 保存的文件列表
        original_file: 原始文件路径
    """
    report_path = os.path.join(output_dir, "分割报告.txt")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("Excel文件分割报告\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"原始文件: {original_file}\n")
        f.write(f"分割时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"分割文件数量: {len(saved_files)}\n")
        f.write(f"输出目录: {output_dir}\n\n")
        f.write("分割文件详情:\n")
        
        for i, file_path in enumerate(saved_files, 1):
            file_name = os.path.basename(file_path)
            f.write(f"{i:2d}. {file_name}\n")
    
    print(f"分割报告已保存: {report_path}")

# 使用示例
if __name__ == "__main__":
    # 输入文件路径
    input_file = "your_excel_file.xlsx"
    
    # 输出目录
    output_directory = "output_parts"
    
    # 每个文件的最大行数
    rows_per_file = 5000  # 可以根据需要调整
    
    # 自定义所需列（可选）
    custom_columns = ['监测名单', '证件号码', '类型']
    
    try:
        # 执行合并和分割
        saved_files = extract_merge_and_split_advanced(
            input_file, 
            output_directory,
            chunk_size=rows_per_file,
            required_columns=custom_columns,
            include_source=True,  # 包含来源Sheet信息
            file_prefix="part",   # 文件前缀
            timestamp=True        # 在文件名中添加时间戳
        )
        
        # 创建分割报告
        create_summary_report(output_directory, saved_files, input_file)
        
        print(f"\n成功保存了 {len(saved_files)} 个文件到目录: {output_directory}")
        
    except Exception as e:
        print(f"处理过程中出错: {str(e)}")