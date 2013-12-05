/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package br.gov.incra.migracao;

import java.io.Serializable;
import java.math.BigDecimal;
import javax.xml.bind.annotation.XmlRootElement;

/**
 *
 * @author waldenilson
 */
public class Tbpecastecnicas implements Serializable {
    private static final long serialVersionUID = 1L;
    private String cdpeca;
    private String nrcontrato;
    private String nrentrega;
    private String nrcpfrequerente;
    private String nmrequerente;
    private String stEnviadoBrasilia;
    private String stPecaTecnica;
    private String stAnexadoProcesso;
    private String dsObservacao;
    private String cdPastaGeo;
    // @Max(value=?)  @Min(value=?)//if you know range of your decimal fields consider using these annotations to enforce field validation
    private BigDecimal nrArea;
    private BigDecimal nrPerimetro;
    private String nmGleba;
    private Integer id;

    public Tbpecastecnicas() {
    }

    public Tbpecastecnicas(Integer id) {
        this.id = id;
    }

    public Tbpecastecnicas(Integer id, String cdpeca) {
        this.id = id;
        this.cdpeca = cdpeca;
    }

    public String getCdpeca() {
        return cdpeca;
    }

    public void setCdpeca(String cdpeca) {
        this.cdpeca = cdpeca;
    }

    public String getNrcontrato() {
        return nrcontrato;
    }

    public void setNrcontrato(String nrcontrato) {
        this.nrcontrato = nrcontrato;
    }

    public String getNrentrega() {
        return nrentrega;
    }

    public void setNrentrega(String nrentrega) {
        this.nrentrega = nrentrega;
    }

    public String getNrcpfrequerente() {
        return nrcpfrequerente;
    }

    public void setNrcpfrequerente(String nrcpfrequerente) {
        this.nrcpfrequerente = nrcpfrequerente;
    }

    public String getNmrequerente() {
        return nmrequerente;
    }

    public void setNmrequerente(String nmrequerente) {
        this.nmrequerente = nmrequerente;
    }

    public String getStEnviadoBrasilia() {
        return stEnviadoBrasilia;
    }

    public void setStEnviadoBrasilia(String stEnviadoBrasilia) {
        this.stEnviadoBrasilia = stEnviadoBrasilia;
    }

    public String getStPecaTecnica() {
        return stPecaTecnica;
    }

    public void setStPecaTecnica(String stPecaTecnica) {
        this.stPecaTecnica = stPecaTecnica;
    }

    public String getStAnexadoProcesso() {
        return stAnexadoProcesso;
    }

    public void setStAnexadoProcesso(String stAnexadoProcesso) {
        this.stAnexadoProcesso = stAnexadoProcesso;
    }

    public String getDsObservacao() {
        return dsObservacao;
    }

    public void setDsObservacao(String dsObservacao) {
        this.dsObservacao = dsObservacao;
    }

    public String getCdPastaGeo() {
        return cdPastaGeo;
    }

    public void setCdPastaGeo(String cdPastaGeo) {
        this.cdPastaGeo = cdPastaGeo;
    }

    public BigDecimal getNrArea() {
        return nrArea;
    }

    public void setNrArea(BigDecimal nrArea) {
        this.nrArea = nrArea;
    }

    public BigDecimal getNrPerimetro() {
        return nrPerimetro;
    }

    public void setNrPerimetro(BigDecimal nrPerimetro) {
        this.nrPerimetro = nrPerimetro;
    }

    public String getNmGleba() {
        return nmGleba;
    }

    public void setNmGleba(String nmGleba) {
        this.nmGleba = nmGleba;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    @Override
    public int hashCode() {
        int hash = 0;
        hash += (id != null ? id.hashCode() : 0);
        return hash;
    }

    @Override
    public boolean equals(Object object) {
        // TODO: Warning - this method won't work in the case the id fields are not set
        if (!(object instanceof Tbpecastecnicas)) {
            return false;
        }
        Tbpecastecnicas other = (Tbpecastecnicas) object;
        if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "br.gov.incra.migracao.Tbpecastecnicas[ id=" + id + " ]";
    }
    
}
