import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { Layout } from 'antd'
import Dashboard from './pages/Dashboard'

const { Header, Content, Sider } = Layout

const App: React.FC = () => {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider width={200} style={{ background: '#fff' }}>
        <div style={{ height: 32, margin: 16, background: 'rgba(0,0,0,.2)' }} />
        <p style={{ padding: '16px', textAlign: 'center', color: '#999' }}>
          导航菜单
        </p>
      </Sider>
      
      <Layout>
        <Header style={{ padding: 0, background: '#fff' }}>
          <div style={{ padding: '0 24px', fontSize: 18, fontWeight: 'bold' }}>
            亚马逊广告智能投放平台
          </div>
        </Header>
        
        <Content style={{ margin: '24px 16px', padding: 24, background: '#fff', minHeight: 280 }}>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/campaigns" element={<div>广告活动管理（开发中）</div>} />
            <Route path="/keywords" element={<div>关键词管理（开发中）</div>} />
            <Route path="/bidding" element={<div>竞价策略（开发中）</div>} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </Content>
      </Layout>
    </Layout>
  )
}

export default App
