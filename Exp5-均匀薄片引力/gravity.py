import numpy as np
import matplotlib.pyplot as plt
# 物理常数
G = 6.67430e-11  # 万有引力常数 (m^3 kg^-1 s^-2)

def calculate_sigma(length, mass):
    """计算面密度"""
    return mass / (length**2)


def integrand(x, y, z):
    """
    被积函数，计算引力积分核
    参数:
        x, y: 薄片上点的坐标 (m)
        z: 测试点高度 (m)
        
    返回:
        积分核函数值
    """
    return 1 / (x**2 + y**2 + z**2)**1.5
    # TODO: 实现积分核函数
    pass

def gauss_legendre_integral(length, z, n_points=100):
    """
    使用高斯-勒让德求积法计算二重积分
    参数:
        length: 薄片边长 (m)
        z: 测试点高度 (m)
        n_points: 积分点数 (默认100)
        
    返回:
        积分结果值
        
    提示:
        1. 使用np.polynomial.legendre.leggauss获取高斯点和权重
        2. 将积分区间从[-1,1]映射到[-L/2,L/2]
        3. 实现双重循环计算二重积分
    """
    # TODO: 实现高斯-勒让德积分
    # 获取高斯点和权重
    xi, wi = np.polynomial.legendre.leggauss(n_points)
    
    # 变换到积分区间 [-L/2, L/2]
    x = xi * (length/2)
    w = wi * (length/2)
    
    # 计算二重积分
    integral = 0.0
    for i in range(n_points):
        for j in range(n_points):
            integral += w[i] * w[j] * integrand(x[i], x[j], z)
            
    return integral
    pass

def calculate_force(length, mass, z, method='gauss'):
    """
    计算给定高度处的引力
    参数:
        length: 薄片边长 (m)
        mass: 薄片质量 (kg)
        z: 测试点高度 (m)
        method: 积分方法 ('gauss'或'scipy')
        
    返回:
        引力值 (N)
    """
    sigma = calculate_sigma(length, mass)
    
    if method == 'gauss':
        integral = gauss_legendre_integral(length, z)
    else:
        # 可以使用scipy作为备选方案
        from scipy.integrate import dblquad
        integral, _ = dblquad(lambda y, x: integrand(x, y, z),
                            -length/2, length/2,
                            lambda x: -length/2, lambda x: length/2)
    
    return G * sigma * z * integral

    # TODO: 调用面密度计算函数
    # TODO: 根据method选择积分方法
    # TODO: 返回最终引力值
    pass

def plot_force_vs_height(length, mass, z_min=0.1, z_max=10, n_points=100):
    """
    绘制引力随高度变化的曲线
    """
    # TODO: 生成高度点数组
    # TODO: 计算各高度点对应的引力
    # TODO: 绘制曲线图
    # TODO: 添加理论极限线
    # TODO: 设置图表标题和标签
    # Generate height points
    z_values = np.linspace(z_min, z_max, n_points)
    
    # Calculate force using both methods
    F_gauss = [calculate_force(length, mass, z, method='gauss') for z in z_values]
    F_scipy = [calculate_force(length, mass, z, method='scipy') for z in z_values]
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(z_values, F_gauss, 'r-', label='Gauss-Legendre')
    plt.plot(z_values, F_scipy, 'g:', label='Scipy dblquad')
    
    # Add theoretical limit line
    sigma = calculate_sigma(length, mass)
    plt.axhline(y=2*np.pi*G*sigma, color='r', linestyle=':', 
               label='z→0 limit (2πGσ)')
    
    plt.xlabel('Height z (m)')
    plt.ylabel('Gravitational Force F_z (N)')
    plt.title('Comparison of Integration Methods')
    plt.legend()
    plt.grid(True)
    plt.show()

def compare_integration_methods(length, mass, z_values):
    """Compare Gauss-Legendre and scipy dblquad integration methods"""
    results = []
    for z in z_values:
        # Calculate using both methods
        gauss_result = calculate_force(length, mass, z, method='gauss')
        scipy_result = calculate_force(length, mass, z, method='scipy')
        
        # Calculate relative difference
        diff = abs(gauss_result - scipy_result)
        rel_diff = diff / scipy_result if scipy_result != 0 else 0
        
        results.append({
            'z': z,
            'gauss': gauss_result,
            'scipy': scipy_result,
            'difference': diff,
            'relative_difference': rel_diff
        })
    
    # Print comparison table
    print("\nIntegration Method Comparison:")
    print("-" * 80)
    print(f"{'z (m)':<10}{'Gauss (N)':<20}{'Scipy (N)':<20}{'Diff':<15}{'Rel Diff':<15}")
    print("-" * 80)
    for r in results:
        print(f"{r['z']:<10.3f}{r['gauss']:<20.6e}{r['scipy']:<20.6e}"
              f"{r['difference']:<15.6e}{r['relative_difference']:<15.6e}")

    pass

# 示例使用
if __name__ == '__main__':
    # 参数设置 (边长10m，质量1e4kg)
    length = 10
    mass = 1e4
    
    # 计算并绘制引力曲线
    plot_force_vs_height(length, mass)
    
    # 打印几个关键点的引力值
    for z in [0.1, 1, 5, 10]:
        F = calculate_force(length, mass, z)
        print(f"高度 z = {z:.1f}m 处的引力 F_z = {F:.3e} N")
    # 测试点
    test_z = [0.1, 0.5, 1, 2, 5, 10]
    
    # 比较积分方法
    compare_integration_methods(length, mass, test_z)
    
